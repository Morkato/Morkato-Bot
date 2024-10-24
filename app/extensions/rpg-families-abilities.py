from morkato.ability import AbilityFlags
from morkato.work.project import registry
from morkato.utils import NoNullDict
from morkato.types import (
  AbilityType,
  NpcType
)
from app.extension import BaseExtension
from discord.interactions import Interaction
from discord import app_commands as apc
from enum import Enum
from typing import (
  Optional,
  ClassVar,
  List
)
import app.converters
import app.embeds
import app.checks
import app.errors

class AbilityFlagsChoice(Enum):
  HUMAN = AbilityFlags.HUMAN
  ONI = AbilityFlags.ONI
  HYBRID = AbilityFlags.HYBRID
@registry
class RPGFamiliesAbilities(BaseExtension):
  LANGUAGE: str
  async def setup(self) -> None:
    self.has_guild_perms = app.checks.has_guild_permissions(manage_guild=True)
    self.LANGUAGE = self.builder.PT_BR
  @apc.command(
    name="family-create",
    description="[RPG Utilitários] Cria uma família"
  )
  @apc.guild_only()
  async def family_create(
    self, interaction: Interaction, *,
    name: str,
    npc: NpcType,
    percent: int,
    description: Optional[str],
    banner: Optional[str]
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    if not guild.families.already_loaded():
      await guild.families.resolve()
    family = await guild.create_family(
      name=name,
      npc_kind=npc,
      percent=percent,
      description=description,
      banner=banner
    )
    builder = FamilyBuilder(family)
    embed = await builder.build(0)
    text = self.builder.get_content(self.LANGUAGE, "onFamilyCreate", family.name)
    embed.set_footer(text=text, icon_url=interaction.client.user.display_avatar.url)
    await interaction.edit_original_response(embed=embed)
  @apc.command(
    name="family-update",
    description="[RPG Utilitários] Atualiza uma família"
  )
  @apc.guild_only()
  @apc.rename(family_query="family")
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
      text = self.builder.get_content(self.LANGUAGE, "onEmptyKwargsWhenUpdateFamily")
      await interaction.edit_original_response(content=text)
      return
    guild = await self.get_morkato_guild(interaction.guild)
    family = await FamilyConverter()._get_by_guild(guild, family_query)
    builder = FamilyBuilder(family)
    embed = await builder.build(0)
    text = self.builder.get_content(self.LANGUAGE, "onUpdateFamily", family.name)
    embed.set_footer(text=text, icon_url=interaction.client.user.display_avatar.url)
    await interaction.edit_original_response(embed=embed)
  @apc.command(
    name="family-delete",
    description="[RPG Utilitários] Deleta uma família"
  )
  @apc.guild_only()
  @apc.rename(family_query="family")
  async def family_delete(
    self, interaction: Interaction, *,
    family_query: str
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    family = await FamilyConverter()._get_by_guild(guild, family_query)
    builder = FamilyBuilder(family)
    embed = await builder.build(0)
    text = self.builder.get_content(self.LANGUAGE, "onFamilyDelete", family.name)
    embed.set_footer(text=text, icon_url=interaction.client.user.display_avatar.url)
    await interaction.edit_original_response(embed=embed)
  @apc.command(
    name="ability-create",
    description="[RPG Utilitários] Cria uma nova habilidade."
  )
  @apc.guild_only()
  async def ability_create(
    self, interaction: Interaction, *,
    name: str,
    percent: int,
    energy: Optional[int],
    description: Optional[str],
    banner: Optional[str]
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    ability = await guild.create_ability(
      name = name,
      energy = energy,
      percent = percent,
      npc_kind = 0,
      description = description,
      banner = banner
    )
    content = self.builder.safe_get_content(self.LANGUAGE, "onAbilityCreate", ability.name)
    embed = await app.embeds.AbilityBuilder(ability).build(0)
    embed.set_footer(
      text=content,
      icon_url=interaction.client.user.display_avatar.url
    )
    await interaction.edit_original_response(embed=embed)
  @apc.command(
    name="ability-update",
    description="[RPG Utilitários] Atualiza a habilidade requerida."
  )
  @apc.guild_only()
  @apc.rename(ability_query="ability")
  async def ability_update(
    self, interaction: Interaction, *,
    ability_query: str,
    name: Optional[str],
    energy: Optional[int],
    percent: Optional[int],
    description: Optional[str],
    banner: Optional[str]
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    ability = await self.convert(app.converters.AbilityConverter, interaction, ability_query, abilities=guild.abilities)
    kwargs = NoNullDict(
      name = name,
      energy = energy,
      percent = percent,
      description = description,
      banner = banner
    )
    if not kwargs:
      content = self.builder.get_content(self.LANGUAGE, "onEmptyKwargsWhenUpdateAbility")
      await interaction.edit_original_response(content=content)
      return
    await ability.update(**kwargs)
    content = self.builder.safe_get_content(self.LANGUAGE, "onAbilityUpdate", ability.name)
    builder = app.embeds.AbilityUpdated(ability)
    await self.send_embed(interaction, builder, resolve_all=True)
  @apc.command(
    name="ability-delete",
    description="[RPG Utilitários] Deleta a habilidade escolhida."
  )
  @apc.guild_only()
  @apc.rename(ability_query="ability")
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
  @apc.command(
    name="sync-ability",
    description="[RPG Utilitários] Sincroniza uma habilidade com uma família"
  )
  @apc.guild_only()
  @apc.rename(family_query="family", ability_query="ability")
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
  @apc.command(
    name = "active-ability-roll",
    description = "[RPG Utilitários] Ativa a habilidade em um roll"
  )
  @apc.rename(ability_query="ability")
  async def activate_ability_roll(
    self, interaction: Interaction, *,
    ability_query: str,
    npc: AbilityFlagsChoice
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    ability = await self.convert(app.converters.AbilityConverter, interaction, ability_query, abilities=guild.abilities)
    flags = ability.npc_type
    if flags.hasflag(npc.value):
      raise app.errors.AppError("onAbilityHasFlag")
    flags.set(npc.value)
    await ability.update(npc_kind=flags)
    content = self.builder.get_content(self.LANGUAGE, "onAbilitySetFlag")
    await interaction.edit_original_response(content=content)