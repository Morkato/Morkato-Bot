from morkbmt.extension import (ExtensionCommandBuilder, Converter)
from morkbmt.context import MorkatoContext
from morkbmt.bot import MorkatoBot
from morkbmt.core import registry
from morkato.errors import UserNotFoundError
from morkato.family import Family
from morkato.user import User
from app.extension import BaseExtension
from typing_extensions import Self
from typing import (
  Coroutine,
  Callable,
  Optional,
  Dict,
  Any
)
from enum import Enum
import discord.ext.commands
import discord
import app.embeds
import app.errors
import app.utils

class FamilyOption(Enum):
  ROLL = "roll"
  SIMULATE = "simulate"
  GET = "get"
  ME = "me"

@registry
class RPGFamiliesExtension(BaseExtension):
  tofamily: Converter[Family]
  async def setup(self, commands: ExtensionCommandBuilder[Self]) -> None:
    self.LANGUAGE = self.msgbuilder.PT_BR
    self.manage_guild_perms = discord.ext.commands.has_guild_permissions(manage_guild=True)
    family_create = commands.app_command("family-create", self.family_create, description="[RPG Utilitários] Cria uma nova família.")
    family_update = commands.app_command("family-update", self.family_update, description="[RPG Utilitários] Atualiza a família requisitada.")
    family_delete = commands.app_command("family-delete", self.family_delete, description="[RPG Utilitários] Excluí a família requisitada.")
    family = commands.command("family", self.family)

    commands.guild_only(family_create)
    commands.guild_only(family_update)
    commands.guild_only(family_delete)
    commands.guild_only(family)

    commands.check(family_create, self.manage_guild_perms)
    commands.check(family_update, self.manage_guild_perms)
    commands.check(family_delete, self.manage_guild_perms)
    commands.check(family, self.manage_guild_perms)

    commands.rename(family_update, family_query="family")
    commands.rename(family_delete, family_query="family")

    self.families_options: Dict[FamilyOption, Callable[..., Coroutine[Any, Any, Any]]] = {
      FamilyOption.ROLL: self.family_roll,
      FamilyOption.SIMULATE: self.family_simulate,
      FamilyOption.GET: self.family_get,
      FamilyOption.ME: self.family_me
    }
  def family_filter(self, user: User) -> Callable[[Family], bool]:
    def predicate(family: Family) -> bool:
      flag = family.user_type[user.type]
      return family.user_type.hasflag(flag) and not family.id in user.families_id
    return predicate
  async def family_roll(self, ctx: MorkatoContext, query: Optional[str]) -> None:
    guild = await self.get_morkato_guild(ctx.guild)
    user = guild.get_cached_user(ctx.author.id)
    try:
      if user is None:
        user = await guild.fetch_user(ctx.author.id)
    except UserNotFoundError:
      user = await app.utils.send_user_registry(ctx, guild)
      if user is None:
        return
    family: Family
    family = await app.utils.roll(guild.families, filter=self.family_filter(user))
    is_valid = user.family_roll != 0
    if is_valid:
      await user.sync_family(family)
      await user.update(family_roll = user.family_roll - 1)
    builder = app.embeds.FamilyRegistryUser(family, is_valid)
    await ctx.send_embed(builder, resolve_all=True)
  async def family_simulate(self, ctx: MorkatoContext, query: Optional[str]) -> None:
    quantity = int(query)
    if not quantity in range(1, 1000000):
      content = self.msgbuilder.get_content(self.LANGUAGE, "onQuantityOutRangeForSimRoll")
      await ctx.send(content)
      return
    guild = await self.get_morkato_guild(ctx.guild)
    rolled_families: Dict[int, int] = {}
    try:
      for i in range(quantity):
        family = await app.utils.roll(guild.families)
        rolled: Optional[int] = rolled_families.get(family.id)
        rolled = 1 if rolled is None else rolled + 1
        rolled_families[family.id] = rolled
    except app.errors.ModelsEmptyError:
      raise app.errors.AppError("familyRollEmpty")
    families = sorted(guild.families, key=lambda family: len(family.name))
    result = app.embeds.FamilyRolledBuilder(
      models = families,
      rolled = rolled_families,
      quantity = quantity
    )
    await ctx.send_embed(result, resolve_all=True)
  async def family_get(self, ctx: MorkatoContext, query: Optional[str]) -> None:
    if query is None:
      return
    guild = await self.get_morkato_guild(ctx.guild)
    family = await self.tofamily(query, families=guild.families)
    builder = app.embeds.FamilyBuilder(family)
    await ctx.send_embed(builder, resolve_all=True)
  async def family_me(self, ctx: MorkatoContext, query: Optional[str]) -> None: ...
  async def family(self, ctx: MorkatoContext, opt: Optional[FamilyOption], *, query: Optional[str]) -> None:
    if opt is None:
      opt = FamilyOption.GET if query is not None else FamilyOption.ROLL
    handler = self.families_options[opt]
    await handler(ctx, query)

  async def family_create(
    self, interaction: discord.Interaction[MorkatoBot], /,
    name: str,
    percent: Optional[int],
    description: Optional[str],
    banner: Optional[str]
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    family = await guild.create_family(
      name = name,
      percent = percent,
      description = description,
      banner = banner
    )
    builder = app.embeds.FamilyCreated(family)
    await self.send_embed(interaction, builder, resolve_all=True)

  async def family_update(
    self, interaction: discord.Interaction[MorkatoBot], /,
    family_query: str,
    name: Optional[str],
    percent: Optional[int],
    description: Optional[str],
    banner: Optional[str]
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    family = await self.tofamily(family_query, families=guild.families)
    await family.update(
      name = name,
      percent = percent,
      description = description,
      banner = banner
    )
    builder = app.embeds.FamilyUpdated(family)
    await self.send_embed(interaction, builder, resolve_all=True)
  
  async def family_delete(
    self, interaction: discord.Interaction[MorkatoBot], /,
    family_query: str,
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    family = await self.tofamily(family_query, families=guild.families)
    await family.delete()
    builder = app.embeds.FamilyDeleted(family)
    await self.send_embed(interaction, builder, resolve_all=True)