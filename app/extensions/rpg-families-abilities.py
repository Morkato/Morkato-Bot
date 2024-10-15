from morkato.ability import AbilityIntents
from morkato.work.project import registry
from morkato.utils import NoNullDict
from morkato.types import (
  AbilityType,
  NpcType
)
from app.utils import (
  FamilyConverter,
  AbilityConverter
)
from discord.interactions import Interaction
from discord import app_commands as apc
from app.extension import BaseExtension
from app.embeds import FamilyBuilder
from typing import (
  Optional,
  ClassVar,
  List
)
import app.embeds
import app.checks
import app.errors

has_guild_perms = app.checks.has_guild_permissions(manage_guild=True)
@registry
class RPGFamiliesAbilities(BaseExtension):
  LANGUAGE: str
  ACTIVATE_ROLL_CHOICES: ClassVar[List[apc.Choice[int]]] = [
    apc.Choice(
      name = "Humano",
      value = AbilityIntents.HUMAN,
    ),
    apc.Choice(
      name = "Oni",
      value = AbilityIntents.ONI
    ),
    apc.Choice(
      name = "Híbrido",
      value = AbilityIntents.HYBRID
    )
  ]
  async def setup(self) -> None:
    self.LANGUAGE = self.builder.PT_BR
  @apc.command(
    name="family-create",
    description="[RPG Utilitários] Cria uma família"
  )
  @apc.guild_only()
  @apc.check(has_guild_perms)
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
  @apc.check(has_guild_perms)
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
  @apc.check(has_guild_perms)
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
    name="set-family",
    description="[RPG Utilitários] Define sua família"
  )
  @apc.guild_only()
  @apc.rename(family_query="family")
  async def set_family(
    self, interaction: Interaction, *,
    family_query: str
  ) -> None:
    await interaction.response.pong()
    guild = await self.get_morkato_guild(interaction.guild)
    player = guild.get_cached_player(interaction.user.id)
    if player is None:
      player = await guild.fetch_player(interaction.user.id)
    if player.family_id is not None:
      raise app.errors.PlayerAlreadyRegisteredFamily(player)
    if player.family_roll != 0:
      raise app.errors.PlayerHasFamilyRolls(player)
    family = await FamilyConverter()._get_by_guild(guild, family_query)
    if not player.has_family(family):
      raise app.errors.DoNotPlayerHasFamily(player, family)
    await player.update(family=family)
    content = self.builder.get_content(self.LANGUAGE, "onSyncFamilyWithPlayer", family.name, interaction.user.name)
    if interaction.response.is_done():
      await interaction.followup.send(content)
      return
    await interaction.response.send_message(content)

  @apc.command(
    name="ability-create",
    description="[RPG Utilitários] Cria uma nova habilidade."
  )
  @apc.guild_only()
  @apc.check(has_guild_perms)
  async def ability_create(self, interaction: Interaction, name: str, type: AbilityType, percent: int, *, description: Optional[str], banner: Optional[str]) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    ability = await guild.create_ability(
      name = name,
      type = type,
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
  @apc.check(has_guild_perms)
  @apc.rename(ability_query="ability")
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
    ability = await AbilityConverter()._get_by_guild(guild, ability_query)
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
    content = self.builder.safe_get_content(self.LANGUAGE, "onAbilityUpdate", ability.name)
    embed = await app.embeds.AbilityBuilder(ability).build(0)
    embed.set_footer(
      text=content,
      icon_url=interaction.client.user.display_avatar.url
    )
    await interaction.edit_original_response(embed=embed)
  @apc.command(
    name="ability-delete",
    description="[RPG Utilitários] Deleta a habilidade escolhida."
  )
  @apc.guild_only()
  @apc.check(has_guild_perms)
  @apc.rename(ability_query="ability")
  async def ability_delete(
    self, interaction: Interaction, *,
    ability_query: str
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    ability = await AbilityConverter()._get_by_guild(guild, ability_query)
    await ability.delete()
    content = self.builder.safe_get_content(self.LANGUAGE, "onAbilityDelete", ability.name)
    embed = await app.embeds.AbilityBuilder(ability).build(0)
    embed.set_footer(
      text=content,
      icon_url=interaction.client.user.display_avatar.url
    )
    await interaction.edit_original_response(embed=embed)
  @apc.command(
    name="ability-sync",
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
    family = await FamilyConverter()._get_by_guild(guild, family_query)
    ability = await AbilityConverter()._get_by_guild(guild, ability_query)
    await family.sync_ability(ability)
    await interaction.response.send_message("A habilidade chamada: **%s** foi sincronizada com a família: **%s**." % (ability.name, family.name))
  @apc.command(
    name = "active-ability-roll",
    description = "[RPG Utilitários] Ativa a habilidade em um roll"
  )
  @apc.choices(npc=ACTIVATE_ROLL_CHOICES)
  @apc.rename(ability_query="ability")
  async def activate_ability_roll(
    self, interaction: Interaction, *,
    ability_query: str,
    npc: apc.Choice[int]
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    ability = await AbilityConverter()._get_by_guild(guild, ability_query)
    intents = ability.npc_kind
    if intents.has_intent(npc.value):
      content = self.builder.get_content(self.LANGUAGE, "onAbilityHasIntent")
      await interaction.edit_original_response(content=content)
      return
    intents.set(npc.value)
    await ability.update(npc_kind=intents)
    content = self.builder.get_content(self.LANGUAGE, "onAbilitySetIntent")
    await interaction.edit_original_response(content=content)
