from morkato.work.context import MorkatoContext
from morkato.work.extension import command
from morkato.work.project import registry
from morkato.abc import UnresolvedSnowflakeList
from morkato.errors import PlayerNotFoundError
from morkato.ability import Ability
from morkato.family import Family
from morkato.player import Player
from morkato.guild import Guild
from app.interfaces import ObjectWithPercentT
from app.extension import BaseExtension
from app.view import RegistryPlayerUi
from random import randint
from typing import (
  Optional,
  Callable,
  Dict
)
import app.converters
import app.embeds
import app.errors

@registry
class RPGRolls(BaseExtension):
  LANGUAGE: str
  async def setup(self) -> None:
    self.LANGUAGE = self.builder.PT_BR
  async def registry_family(self, ctx: MorkatoContext, player: Player) -> Family:
    families = sorted(player._families.values(), key=lambda family: len(family.name), reverse=True)
    if len(families) == 0:
      raise NotImplementedError
    family = await ctx.send_select_menu(
      models=families,
      title=self.builder.safe_get_content(self.LANGUAGE, "familySelectMenuTitle"),
      description=self.builder.get_content(self.LANGUAGE, "familySelectMenuDescription", user=ctx.author),
      selected_line_style=self.builder.get_content_unknown_formatting(self.LANGUAGE, "familySelectMenuSelectedLineStyle"),
      line_style=self.builder.get_content_unknown_formatting(self.LANGUAGE, "familySelectMenuNotSelectedLineStyle"),
      key=lambda family: app.embeds.FamilyBuilder(family)
    )
    await player.update(family=family)
    content = self.get_content(self.LANGUAGE, "onRegistryPlayerFamily", ctx.author.name, family.name)
    await ctx.send(content)
    return family
  async def registry_player(self, ctx: MorkatoContext, guild: Guild) -> Optional[Player]:
    embed = await app.embeds.PlayerChoiceTypeBuilder().build(0)
    view = RegistryPlayerUi(guild, ctx.bot.loop)
    message = await ctx.send(embed=embed, view=view)
    player = await view.get()
    await message.delete()
    return player
  async def get_or_registry_player(self, ctx: MorkatoContext, guild: Guild) -> Player:
    try:
      return await self.get_cached_or_fetch_player(guild, ctx.author.id)
    except PlayerNotFoundError:
      return await self.registry_player(ctx, guild)
  async def roll(
    self, models: UnresolvedSnowflakeList[ObjectWithPercentT], *,
    filter: Optional[Callable[[ObjectWithPercentT], bool]] = None
  ) -> ObjectWithPercentT:
    await self.resolve(models)
    if len(models) == 0:
      raise app.errors.AppError("modelsIsEmpty")
    objs = [elem for elem in models if filter(elem)] if filter is not None else models
    if len(objs) == 0:
      raise app.errors.AppError("modelsIsEmpty")
    total = sum(obj.percent for obj in objs)
    generated = randint(0, total)
    current = 0
    for obj in objs:
      current += obj.percent
      is_valid = 0 >= generated - current
      if is_valid:
        break
    return obj
  def filter_family(self, player: Player, family: Family) -> bool:
    return (
      family.npc_type.hasflag(getattr(family.npc_type, player.npc_type))
        and not player.has_family(family)
    )
  def filter_ability(self, player: Player, ability: Ability) -> bool:
    return (
      player.family.get_ability(ability.id) is None
        and not player.has_ability(ability)
        and ability.npc_type.hasflag(getattr(ability.npc_type, player.npc_type))
    )
  @command(
    name = "sim-ability-roll",
    description = "[RPG] Simula os rolls de habilidade."
  )
  async def sim_ability_roll(self, ctx: MorkatoContext, /, quantity: int) -> None:
    if not quantity in range(1, 1000000):
      content = self.get_content(self.LANGUAGE, "onQuantityOutRangeForSimRoll")
      await ctx.send(content)
      return
    guild = await self.get_morkato_guild(ctx.guild)
    await self.resolve(guild.abilities)
    rolled_abilities: Dict[int, int] = {}
    for i in range(quantity):
      ability = await self.roll(guild.abilities)
      rolled: Optional[int] = rolled_abilities.get(ability.id)
      rolled = 1 if rolled is None else rolled + 1
      rolled_abilities[ability.id] = rolled
    abilities = sorted(guild.abilities, key=lambda ability: len(ability.name))
    result = app.embeds.AbilityRolledBuilder(
      models = abilities,
      rolled = rolled_abilities,
      quantity = quantity
    )
    await ctx.send_embed(result, resolve_all=True)
  @command(
    name = "sim-family-roll",
    description = "[RPG] Simula os rolls de famílias."
  )
  async def sim_family_roll(self, ctx: MorkatoContext, /, quantity: int) -> None:
    if not quantity in range(1, 1000000):
      content = self.builder.get_content(self.LANGUAGE, "onQuantityOutRangeForSimRoll")
      await ctx.send(content)
      return
    guild = await self.get_morkato_guild(ctx.guild)
    await self.resolve(guild.families)
    rolled_families: Dict[int, int] = {}
    for i in range(quantity):
      family = await self.roll(guild.families)
      rolled: Optional[int] = rolled_families.get(family.id)
      rolled = 1 if rolled is None else rolled + 1
      rolled_families[family.id] = rolled
    families = sorted(guild.families, key=lambda family: len(family.name))
    result = app.embeds.FamilyRolledBuilder(
      models = families,
      rolled = rolled_families,
      quantity = quantity
    )
    await ctx.send_embed(result, resolve_all=True)
  @command(name="family")
  async def family(self, ctx: MorkatoContext) -> None:
    guild = await self.get_morkato_guild(ctx.guild)
    await self.resolve(guild.families)
    if len(guild.families) == 0:
      raise app.errors.AppError("onFamilyEmpty")
    player = await self.get_or_registry_player(ctx, guild)
    family = await self.roll(guild.families, filter=lambda family: self.filter_family(player, family))
    is_valid = player.family_roll != 0
    if is_valid:
      await player.sync_family(family)
    builder = app.embeds.FamilyRegistryPlayer(family, is_valid)
    await ctx.send_embed(builder, resolve_all=True)
  @command(name="ability")
  async def ability(self, ctx: MorkatoContext, *, ability_query: Optional[str]) -> None:
    guild = await self.get_morkato_guild(ctx.guild)
    if ability_query is not None:
      ability = await self.convert(app.converters.AbilityConverter, ctx, ability_query, abilities=guild.abilities)
      builder = app.embeds.AbilityBuilder(ability)
      await ctx.send_embed(builder)
      return
    await self.resolve(guild.abilities)
    if len(guild.abilities) == 0:
      raise app.errors.AppError("onAbilityEmpty")
    player = await self.get_cached_or_fetch_player(guild, ctx.author.id)
    if player.family is None:
      if player.family_roll != 0:
        raise app.errors.AppError("onUnChoiceFamilyPlayerForRollAbilityHasRolls", player.family_roll)
      await self.registry_family(ctx, player)
    ability = await self.roll(guild.abilities, filter=lambda ability: self.filter_ability(player, ability))
    is_valid = player.ability_roll != 0
    if is_valid:
      await player.sync_ability(ability)
    builder = app.embeds.AbilityRegistryPlayer(ability, is_valid)
    await ctx.send_embed(builder, resolve_all=True)
  @command(name="prodigy")
  async def prodigy(self, ctx: MorkatoContext) -> None:
    guild = await self.get_morkato_guild(ctx.guild)
    player = await self.get_cached_or_fetch_player(guild, ctx.author.id)
    flags = player.flags
    if flags.prodigy():
      raise app.errors.AppError("onPlayerAlreadyIsProdigy")
    if player.prodigy_roll == 0:
      raise app.errors.AppError("onPlayerEmptyProdigyRoll")
    generated = randint(0, 5)
    if generated != 1:
      await player.update(prodigy_roll=player.prodigy_roll - 1)
      raise app.errors.AppError("onPlayerGetUpProdigy")
    new_flags = flags.copy()
    new_flags.set(flags.PRODIGY)
    await player.update(prodigy_roll=player.prodigy_roll - 1, flags=new_flags)
    content = self.get_content(self.LANGUAGE, "onPlayerGetProdigy")
    await ctx.send(content)
  @command(name="mark")
  async def mark(self, ctx: MorkatoContext) -> None:
    guild = await self.get_morkato_guild(ctx.guild)
    player = await self.get_cached_or_fetch_player(guild, ctx.author.id)
    flags = player.flags
    if flags.mark():
      raise app.errors.AppError("onPlayerAlreadyIsMark")
    if player.mark_roll == 0:
      raise app.errors.AppError("onPlayerEmptyMarkRoll")
    generated = randint(0, 20)
    if generated != 1:
      await player.update(mark_roll=player.mark_roll - 1)
      raise app.errors.AppError("onPlayerGetUpMark")
    new_flags = flags.copy()
    new_flags.set(flags.MARK)
    await player.update(mark_roll=player.mark_roll - 1, flags=new_flags)
    content = self.get_content(self.LANGUAGE, "onPlayerGetMark")
    await ctx.send(content)
  @command(name="berserk")
  async def berserk(self, ctx: MorkatoContext) -> None:
    guild = await self.get_morkato_guild(ctx.guild)
    player = await self.get_cached_or_fetch_player(guild, ctx.author.id)
    flags = player.flags
    if flags.berserk():
      raise app.errors.AppError("onPlayerAlreadyIsBerserk")
    if player.berserk_roll == 0:
      raise app.errors.AppError("onPlayerEmptyBerserkRoll")
    generated = randint(0, 20)
    if generated != 1:
      await player.update(berserk_roll=player.berserk_roll - 1)
      raise app.errors.AppError("onPlayerGetUpBerserk")
    new_flags = flags.copy()
    new_flags.set(flags.BERSERK)
    await player.update(berserk_roll=player.berserk_roll - 1, flags=new_flags)
    content = self.get_content(self.LANGUAGE, "onPlayerGetBerserk")
    await ctx.send(content)
  @command(name="attack", aliases=["a"])
  async def attack(self, ctx: MorkatoContext, *, attack_query: str) -> None:
    guild = await self.get_morkato_guild(ctx.guild)
    attack = await self.convert(app.converters.AttackConverter, ctx, attack_query, arts=guild.arts, attacks=guild._attacks)
    builder = app.embeds.AttackBuilder(attack)
    await ctx.send_embed(builder, resolve_all=True)
  @command(name="me")
  async def me(self, ctx: MorkatoContext) -> None:
    guild = await self.get_morkato_guild(ctx.guild)
    player = await self.get_cached_or_fetch_player(guild, ctx.author.id)
    npc = player.npc
    if npc is None:
      raise app.errors.AppError("unregistedPlayer")
    builder = app.embeds.NpcCardBuilder(npc)
    await ctx.send_embed(builder, resolve_all=True)