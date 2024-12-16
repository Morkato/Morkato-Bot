from morkbmt.context import MorkatoContext
from morkbmt.extension import (ExtensionCommandBuilder, Converter, command)
from morkbmt.core import registry
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
from typing_extensions import Self
from typing import (
  Optional,
  Callable,
  ClassVar,
  Dict
)
import app.embeds
import app.errors

@registry
class RPGRollsExtension(BaseExtension):
  LANGUAGE: ClassVar[str]
  tofamily: Converter[Family]
  toability: Converter[Ability]
  async def setup(self, commands: ExtensionCommandBuilder[Self]) -> None:
    self.LANGUAGE = self.msgbuilder.PT_BR
    sim_ability_roll = commands.command("sim-ability-roll", self.sim_ability_roll, description="[RPG] Simula rolls de habilidade.")
    sim_family_roll = commands.command("sim-family-roll", self.sim_family_roll, description="[RPG] Simula rolls de família.")
    family = commands.command("family", self.family)
    ability = commands.command("ability", self.ability)
    prodigy = commands.command("prodigy", self.prodigy)
    mark = commands.command("mark", self.mark)
    berserk = commands.command("berserk", self.berserk)
    
    commands.guild_only(sim_ability_roll)
    commands.guild_only(sim_family_roll)
    commands.guild_only(family)
    commands.guild_only(ability)
    commands.guild_only(prodigy)
    commands.guild_only(mark)
    commands.guild_only(berserk)
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
    await models.resolve()
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
  async def sim_ability_roll(self, ctx: MorkatoContext, /, quantity: int) -> None:
    if not quantity in range(1, 1000000):
      content = self.get_content(self.LANGUAGE, "onQuantityOutRangeForSimRoll")
      await ctx.send(content)
      return
    guild = await self.get_morkato_guild(ctx.guild)
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
  async def sim_family_roll(self, ctx: MorkatoContext, /, quantity: int) -> None:
    if not quantity in range(1, 1000000):
      content = self.builder.get_content(self.LANGUAGE, "onQuantityOutRangeForSimRoll")
      await ctx.send(content)
      return
    guild = await self.get_morkato_guild(ctx.guild)
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
  async def ability(self, ctx: MorkatoContext, *, ability_query: Optional[str]) -> None:
    guild = await self.get_morkato_guild(ctx.guild)
    if ability_query is not None:
      ability = await self.toability(ability_query, abilities=guild.abilities)
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