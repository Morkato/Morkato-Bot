from morkbmt.extension import (ExtensionCommandBuilder, Converter)
from morkbmt.context import MorkatoContext
from morkbmt.bot import MorkatoBot
from morkbmt.core import registry
from morkato.errors import UserNotFoundError
from morkato.utils import NoNullDict
from morkato.ability import Ability
from morkato.guild import Guild
from morkato.types import UserType
from morkato.user import User
from discord.interactions import Interaction
from app.extension import BaseExtension
from typing_extensions import Self
from typing import (
  Coroutine,
  Optional,
  Callable,
  Dict,
  Any
)
from enum import Enum
import discord.ext.commands
import app.embeds
import app.errors
import app.utils
import app.view

class AbilityOption(Enum):
  ROLL = "roll"
  SIMULATE = "simulate"
  GET = "get"
  ME = "me"

@registry
class RPGAbilitiesExtension(BaseExtension):
  toability: Converter[Ability]
  async def setup(self, commands: ExtensionCommandBuilder[Self]) -> None:
    self.LANGUAGE = self.msgbuilder.PT_BR
    self.manage_guild_perms = discord.ext.commands.has_guild_permissions(manage_guild=True)
    ability_create = commands.app_command("ability-create", self.ability_create, description="[RPG Utilitários] Cria uma nova habilidade.")
    ability_update = commands.app_command("ability-update", self.ability_update, description="[RPG Utilitários] Atualiza a habilidade requisitada.")
    ability_delete = commands.app_command("ability-delete", self.ability_delete, description="[RPG Utilitários] Deleta a habilidade requisitada.")
    active_ability_roll = commands.app_command("active-ability-roll", self.active_ability_roll, description="[RPG Utilitários] Ativa o roll para a habilidade requisitada.")
    ability = commands.command("ability", self.ability)
    
    commands.guild_only(active_ability_roll)
    commands.guild_only(ability_delete)
    commands.guild_only(ability_create)
    commands.guild_only(ability_update)
    commands.guild_only(ability)

    commands.check(active_ability_roll, self.manage_guild_perms)
    commands.check(ability_create, self.manage_guild_perms)
    commands.check(ability_update, self.manage_guild_perms)
    commands.check(ability_delete, self.manage_guild_perms)

    commands.rename(active_ability_roll, ability_query="ability", user_type="user")
    commands.rename(ability_update, ability_query="ability")
    commands.rename(ability_delete, ability_query="ability")

    self.ability_options: Dict[AbilityOption, Callable[..., Coroutine[Any, Any, Any]]] = {
      AbilityOption.GET: self.ability_get,
      AbilityOption.ROLL: self.ability_roll,
      AbilityOption.SIMULATE: self.ability_simulate,
      AbilityOption.ME: self.ability_me
    }
  async def send_user_registry(self, ctx: MorkatoContext, guild: Guild) -> Optional[User]:
    view = app.view.RegistryUserUi(guild, ctx.bot.loop)
    builder = app.embeds.UserRegistryEmbed(ctx.author)
    embed = builder.build(0)
    origin = await ctx.send(embed=embed, view=view)
    resp = await view.get()
    await origin.delete()
    return resp
  def ability_filter(self, user: User) -> Callable[[Ability], bool]:
    def predicate(ability: Ability) -> bool:
      flag = ability.user_type[user.type]
      return ability.user_type.hasflag(flag) and not ability.id in user.abilities_id
    return predicate
  async def ability_get(self, ctx: MorkatoContext, query: Optional[str]) -> None:
    if query is None:
      return
    guild = await self.get_morkato_guild(ctx.guild)
    ability = await self.toability(query, abilities=guild.abilities)
    builder = app.embeds.AbilityBuilder(ability)
    await ctx.send_embed(builder)
  async def ability_roll(self, ctx: MorkatoContext, query: Optional[str]) -> None:
    guild = await self.get_morkato_guild(ctx.guild)
    user = guild.get_cached_user(ctx.author.id)
    try:
      if user is None:
        user = await guild.fetch_user(ctx.author.id)
    except UserNotFoundError:
      user = await self.send_user_registry(ctx, guild)
      if user is None:
        return
    ability: Ability
    try:
      ability = await app.utils.roll(guild.abilities, filter = self.ability_filter(user))
    except app.errors.ModelsEmptyError:
      raise app.errors.AppError("abilityRollEmpty")
    is_valid = user.ability_roll != 0
    if is_valid:
      await user.sync_ability(ability)
      await user.update(ability_roll = user.ability_roll - 1)
    builder = app.embeds.AbilityRegistryUser(ability, is_valid)
    await ctx.send_embed(builder, resolve_all=True)
  async def ability_simulate(self, ctx: MorkatoContext, query: Optional[str]) -> None:
    quantity = int(query)
    if not quantity in range(1, 1000000):
      content = self.msgbuilder.get_content(self.LANGUAGE, "onQuantityOutRangeForSimRoll")
      await ctx.send(content)
      return
    guild = await self.get_morkato_guild(ctx.guild)
    rolled_abilities: Dict[int, int] = {}
    try:
      for i in range(quantity):
        ability = await app.utils.roll(guild.abilities)
        rolled: Optional[int] = rolled_abilities.get(ability.id)
        rolled = 1 if rolled is None else rolled + 1
        rolled_abilities[ability.id] = rolled
    except app.errors.ModelsEmptyError:
      raise app.errors.AppError("abilityRollEmpty")
    abilities = sorted(guild.abilities, key=lambda ability: len(ability.name))
    result = app.embeds.AbilityRolledBuilder(
      models = abilities,
      rolled = rolled_abilities,
      quantity = quantity
    )
    await ctx.send_embed(result, resolve_all=True)
  async def ability_me(self, ctx: MorkatoContext, query: Optional[str]) -> None:
    author = ctx.author
    if query is not None:
      author = await discord.ext.commands.UserConverter().convert(ctx, query)
    guild = await self.get_morkato_guild(ctx.guild)
    user = guild.get_cached_user(author.id)
    try:
      if user is None:
        user = await guild.fetch_user(author.id)
    except UserNotFoundError:
      if ctx.author.id == author.id:
        raise app.errors.AppError("abilityUserEmpty")
      raise app.errors.AppError("abilityOtherUserEmpty", user=author)
    if len(user.abilities_id) == 0:
      if ctx.author.id == author.id:
        raise app.errors.AppError("abilityUserEmpty")
      raise app.errors.AppError("abilityOtherUserEmpty", user=author)
    await guild.abilities.resolve()
    abilities = {
      ability_id: await self.toability(ability_id, abilities = guild.abilities)
      for ability_id in user.abilities_id
    }
    builder = app.embeds.AbilityRollMeBuilder(abilities)
    await ctx.send_embed(builder, resolve_all=True)
  
  async def ability(self, ctx: MorkatoContext, opt: Optional[AbilityOption], *, query: Optional[str]) -> None:
    if opt is None:
      opt = AbilityOption.GET if query else AbilityOption.ROLL
    handler = self.ability_options[opt]
    await handler(ctx, query)

  async def ability_create(
    self, interaction: Interaction[MorkatoBot], /,
    name: str,
    percent: Optional[int],
    description: Optional[str],
    banner: Optional[str]
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    ability = await guild.create_ability(
      name = name,
      percent = percent,
      description = description,
      banner = banner
    )
    builder = app.embeds.AbilityCreated(ability)
    await self.send_embed(interaction, builder, resolve_all=True)
  
  async def ability_update(
    self, interaction: Interaction[MorkatoBot], /,
    ability_query: str,
    name: Optional[str],
    percent: Optional[int],
    description: Optional[str],
    banner: Optional[str]
  ) -> None:
    await interaction.response.defer()
    payload = NoNullDict(
      name = name,
      percent = percent,
      description = description,
      banner = banner
    )
    if not payload:
      raise app.errors.AppError("onEmptyKwargsWhenUpdateAbility")
    guild = await self.get_morkato_guild(interaction.guild)
    ability = await self.toability(ability_query, abilities=guild.abilities)
    await ability.update(**payload)
    builder = app.embeds.AbilityUpdated(ability)
    await self.send_embed(interaction, builder, resolve_all=True)
  
  async def ability_delete(
    self, interaction: Interaction[MorkatoBot], /,
    ability_query: str
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    ability = await self.toability(ability_query, abilities=guild.abilities)
    await ability.delete()
    builder = app.embeds.AbilityDeleted(ability)
    await self.send_embed(interaction, builder, resolve_all=True)
  
  async def active_ability_roll(
    self, interaction: Interaction[MorkatoBot], /,
    ability_query: str,
    user_type: UserType
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    ability = await self.toability(ability_query, abilities=guild.abilities)
    flags = ability.user_type.copy()
    flag = flags[user_type]
    if flags.hasflag(flag):
      raise app.errors.AppError("abilityUserAlreadyActivated", ability=ability)
    flags.set(flag)
    await ability.update(user_type = flags)
    content = self.msgbuilder.get_content(self.LANGUAGE, "abilityUserActivated", ability=ability)
    await interaction.edit_original_response(content=content)