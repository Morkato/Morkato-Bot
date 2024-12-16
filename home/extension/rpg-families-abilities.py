from morkbmt.extension import (ExtensionCommandBuilder, Converter)
from morkbmt.core import registry
from morkato.utils import NoNullDict
from morkato.family import Family
from morkato.ability import Ability
from morkato.npc import NpcTypeFlags
from app.extension import BaseExtension
from discord.ext import commands
from discord.interactions import Interaction
from discord import app_commands as apc
from enum import Enum
from typing_extensions import Self
from typing import (
  Optional,
  ClassVar
)
import discord.ext.commands
import app.embeds
import app.errors

class NpcTypeFlagsChoice(Enum):
  HUMAN = NpcTypeFlags.HUMAN
  ONI = NpcTypeFlags.ONI
  HYBRID = NpcTypeFlags.HYBRID
@registry
class RPGFamiliesAbilities(BaseExtension):
  tofamily: Converter[Family]
  toability: Converter[Ability]
  async def setup(self, commands: ExtensionCommandBuilder[Self]) -> None:
    self.LANGUAGE = self.msgbuilder.PT_BR
    self.manage_guild_perms = discord.ext.commands.has_guild_permissions(manage_guild=True)
    family_create = commands.app_command("family-create", self.family_create, description="[RPG Utilitários] Cria uma família")
    family_update = commands.app_command("family-update", self.family_update, description="[RPG Utilitários] Atualiza uma família")
    family_delete = commands.app_command("family-delete", self.family_delete, description="[RPG Utilitários] Deleta uma família")
    ability_create = commands.app_command("ability-create", self.ability_create, description="[RPG Utilitários] Cria uma nova habilidade.")
    ability_update = commands.app_command("ability-update", self.ability_update, description="[RPG Utilitários] Atualiza a habilidade requisitada.")
    ability_delete = commands.app_command("ability-delete", self.ability_delete, description="[RPG Utilitários] Deleta a habilidade requisitada.")
    ability_sync = commands.app_command("ability-sync", self.ability_sync, description="[RPG Utilitários] Sincroniza a habilidade requisitada com uma família")
    activate_family_roll = commands.app_command("activate-family-roll", self.activate_family_roll, description="[RPG Utilitários] Ativa o roll de uma família para tal raça.")
    activate_ability_roll = commands.app_command("activate-ability-roll", self.activate_ability_roll, description = "[RPG Utilitários] Ativa a habilidade em um roll.")
    
    commands.check(family_create, self.manage_guild_perms)
    commands.check(family_update, self.manage_guild_perms)
    commands.check(family_delete, self.manage_guild_perms)
    commands.check(ability_create, self.manage_guild_perms)
    commands.check(ability_update, self.manage_guild_perms)
    commands.check(ability_delete, self.manage_guild_perms)
    commands.check(ability_sync, self.manage_guild_perms)
    commands.check(activate_family_roll, self.manage_guild_perms)
    commands.check(activate_ability_roll, self.manage_guild_perms)
    
    commands.guild_only(family_create)
    commands.guild_only(family_update)
    commands.guild_only(family_delete)
    commands.guild_only(ability_create)
    commands.guild_only(ability_update)
    commands.guild_only(ability_delete)
    commands.guild_only(ability_sync)
    commands.guild_only(activate_family_roll)
    commands.guild_only(activate_ability_roll)

    commands.rename(family_update, family_query="family")
    commands.rename(family_delete, family_query="family")
    commands.rename(activate_family_roll, family_query="family")
    commands.rename(ability_update, ability_query="ability")
    commands.rename(ability_delete, ability_query="ability")
    commands.rename(activate_ability_roll, ability_query="ability")
    commands.rename(ability_sync, family_query="family", ability_query="ability")
  async def family_create(
    self, interaction: Interaction, *,
    name: str,
    percent: int,
    description: Optional[str],
    banner: Optional[str]
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    family = await guild.create_family(
      name=name,
      npc_type=0,
      percent=percent,
      description=description,
      banner=banner
    )
    builder = app.embeds.FamilyCreated(family)
    await self.send_embed(interaction, builder, resolve_all=True)
  async def family_update(
    self, interaction: Interaction, *,
    family_query: str,
    name: Optional[str],
    percent: Optional[int],
    description: Optional[str],
    banner: Optional[str]
  ) -> None:
    await interaction.response.defer()
    kwargs = NoNullDict(
      name=name,
      percent=percent,
      description=description,
      banner=banner
    )
    if not kwargs:
      raise app.errors.AppError("onEmptyKwargsWhenUpdateFamily")
    guild = await self.get_morkato_guild(interaction.guild)
    family = await self.convert(app.converters.FamilyConverter, interaction, family_query, families=guild.families)
    builder = app.embeds.FamilyUpdated(family)
    await self.send_embed(interaction, builder, resolve_all=True)
  async def family_delete(
    self, interaction: Interaction, *,
    family_query: str
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    family = await self.convert(app.converters.FamilyConverter, interaction, family_query, families=guild.families)
    await family.delete()
    builder = app.embeds.FamilyDeleted(family)
    await self.send_embed(interaction, builder, resolve_all=True)
  async def activate_family_roll(self, interaction: Interaction, *, family_query: str, npc_type: NpcTypeFlagsChoice) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    family = await self.convert(app.converters.FamilyConverter, interaction, family_query, families=guild.families)
    flags = family.npc_type
    if flags.hasflag(npc_type.value):
      raise app.errors.AppError("familyHasFlag")
    new_flags = flags.copy()
    new_flags.set(npc_type.value)
    await family.update(npc_type=new_flags)
    builder = app.embeds.FamilyUpdated(family)
    await self.send_embed(interaction, builder, resolve_all=True)
  async def ability_create(
    self, interaction: Interaction, *,
    name: str,
    percent: int,
    energy: int,
    description: Optional[str],
    banner: Optional[str]
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    ability = await guild.create_ability(
      name = name,
      energy = energy,
      percent = percent,
      npc_type = 0,
      description = description,
      banner = banner
    )
    builder = app.embeds.AbilityBuilder(ability)
    await self.send_embed(interaction, builder, resolve_all=True)
  async def ability_update(
    self, interaction: Interaction, *,
    ability_query: str,
    name: Optional[str],
    percent: Optional[int],
    description: Optional[str],
    banner: Optional[str]
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    ability = await self.convert(app.converters.AbilityConverter, interaction, ability_query, abilities=guild.abilities)
    kwargs = NoNullDict(
      name = name,
      percent = percent,
      description = description,
      banner = banner
    )
    if not kwargs:
      content = self.builder.get_content(self.LANGUAGE, "onEmptyKwargsWhenUpdateAbility")
      await interaction.edit_original_response(content=content)
      return
    await ability.update(**kwargs)
    builder = app.embeds.AbilityUpdated(ability)
    await self.send_embed(interaction, builder, resolve_all=True)
  async def ability_delete(
    self, interaction: Interaction, *,
    ability_query: str
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    ability = await self.convert(app.converters.AbilityConverter, interaction, ability_query, abilities=guild.abilities)
    await ability.delete()
    builder = app.embeds.AbilityDeleted(ability)
    await self.send_embed(interaction, builder, resolve_all=True)
  async def ability_sync(
    self, interaction: Interaction, *,
    family_query: str,
    ability_query: str
  ) -> None:
    await interaction.response.pong()
    guild = await self.get_morkato_guild(interaction.guild)
    family = await self.convert(app.converters.FamilyConverter, interaction, family_query, families=guild.families)
    ability = await self.convert(app.converters.AbilityConverter, interaction, ability_query, abilities=guild.abilities)
    await family.sync_ability(ability)
    content = await self.get_content(self.LANGUAGE, "syncAbilityWithFamily", ability=ability, family=family)
    await interaction.response.send_message(content)
  async def activate_ability_roll(
    self, interaction: Interaction, *,
    ability_query: str,
    npc_type: NpcTypeFlagsChoice
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    ability = await self.convert(app.converters.AbilityConverter, interaction, ability_query, abilities=guild.abilities)
    flags = ability.npc_type
    if flags.hasflag(npc_type.value):
      raise app.errors.AppError("onAbilityHasFlag")
    flags.set(npc_type.value)
    await ability.update(npc_type=flags)
    content = self.builder.get_content(self.LANGUAGE, "onAbilitySetFlag")
    await interaction.edit_original_response(content=content)