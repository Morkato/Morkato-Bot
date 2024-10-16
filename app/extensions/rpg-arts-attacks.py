from morkato.work.extension import command
from morkato.work.project import registry
from morkato.attack import AttackIntents
from morkato.utils import NoNullDict
from morkato.types import ArtType
from discord.interactions import Interaction
from app.extension import BaseExtension
from discord import app_commands as apc
from typing import Optional
from enum import Enum
import app.converters
import app.errors
import app.embeds
import app.checks

class AttackChoiceIntent(Enum):
  UNAVOIDABLE = (1 << 2)
  INDEFENSIBLE = (1 << 3)
  AREA = (1 << 4)
  NOT_COUNTER_ATTACKABLE = (1 << 5)
  COUNTER_ATTACKABLE = (1 << 6)
  DEFENSIVE = (1 << 7)
@registry
class RPGArtsAttacksExtension(BaseExtension):
  LANGUAGE: str
  async def setup(self) -> None:
    self.has_guild_perms = app.checks.has_guild_permissions(manage_guild=True)
    self.LANGUAGE = self.builder.PT_BR
    self.art_create.add_check(self.has_guild_perms)
    self.art_update.add_check(self.has_guild_perms)
    self.attack_create.add_check(self.has_guild_perms)
    self.attack_update.add_check(self.has_guild_perms)
    self.attack_set_intent.add_check(self.has_guild_perms)
    self.attack_reset_intents.add_check(self.has_guild_perms)
  @apc.command(
    name="art-create",
    description="[RPG Utilitários] Cria uma nova arte."
  )
  @apc.guild_only()
  async def art_create(
    self, interaction: Interaction, /, *,
    name: str,
    type: ArtType,
    energy: Optional[int],
    life: Optional[int],
    breath: Optional[int],
    blood: Optional[int],
    description: Optional[str],
    banner: Optional[str]
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    art = await guild.create_art(
      name = name,
      type = type,
      energy = energy,
      life = life,
      breath = breath,
      blood = blood,
      description = description,
      banner = banner
    )
    builder = app.embeds.ArtCreatedBuilder(art)
    await self.send_embed(interaction, builder, resolve_all=True)
  @apc.command(
    name="art-update",
    description="[RPG Utilitários] Atualiza uma arte já existente."
  )
  @apc.rename(art_query="art")
  @apc.guild_only()
  async def art_update(
    self, interaction: Interaction, /, *,
    art_query: str,
    name: Optional[str],
    type: Optional[ArtType],
    energy: Optional[int],
    life: Optional[int],
    breath: Optional[int],
    blood: Optional[int],
    description: Optional[str],
    banner: Optional[str]
  ) -> None:
    await interaction.response.defer()
    kwargs = NoNullDict(
      name = name,
      type = type,
      energy = energy,
      life = life,
      breath = breath,
      blood = blood,
      description = description,
      banner = banner
    )
    if not kwargs:
      raise app.errors.AppError("commandKwargsIsEmpty")
    guild = await self.get_morkato_guild(interaction.guild)
    art = await self.convert(app.converters.ArtConverter, interaction, art_query, arts=guild.arts)
    await art.update(**kwargs)
    builder = app.embeds.ArtUpdatedBuilder(art)
    await self.send_embed(interaction, builder, resolve_all=True)
  @apc.command(
    name="attack-create",
    description="[RPG Utilitários] Cria um novo ataque."
  )
  @apc.rename(art_query="art")
  @apc.guild_only()
  async def attack_create(
    self, interaction: Interaction, /, *,
    art_query: str,
    name: str,
    prefix: Optional[str],
    description: Optional[str],
    banner: Optional[str],
    damage: Optional[int],
    breath: Optional[int],
    blood: Optional[int]
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    art = await self.convert(app.converters.ArtConverter, interaction, art_query, arts=guild.arts)
    attack = await art.create_attack(
      name = name,
      name_prefix_art = prefix,
      description = description,
      banner = banner,
      damage = damage,
      breath = breath,
      blood = blood
    )
    builder = app.embeds.AttackCreatedBuilder(attack)
    await self.send_embed(interaction, builder, resolve_all=True)
  @apc.command(
    name="attack-update",
    description="[RPG Utilitários] Atualiza um ataque já existente."
  )
  @apc.rename(attack_query="attack")
  @apc.guild_only()
  async def attack_update(
    self, interaction: Interaction, /, *,
    attack_query: str,
    name: Optional[str],
    prefix: Optional[str],
    description: Optional[str],
    banner: Optional[str],
    damage: Optional[int],
    breath: Optional[int],
    blood: Optional[int]
  ) -> None:
    await interaction.response.defer()
    kwargs = NoNullDict(
      name = name,
      name_prefix_art = prefix,
      description = description,
      banner = banner,
      damage = damage,
      breath = breath,
      blood = blood
    )
    if not kwargs:
      raise app.errors.AppError("commandKwargsIsEmpty")
    guild = await self.get_morkato_guild(interaction.guild)
    attack = await self.convert(app.converters.AttackConverter, interaction, attack_query, arts=guild.arts, attacks=guild._attacks)
    await attack.update(**kwargs)
    builder = app.embeds.AttackUpdatedBuilder(attack)
    await self.send_embed(interaction, builder, resolve_all=True)
  @apc.command(
    name="attack-set-intent",
    description="[RPG Utilitários] Manipula as intenções de um ataque."
  )
  @apc.rename(attack_query="attack")
  @apc.guild_only()
  async def attack_set_intent(self, interaction: Interaction, attack_query: str, intent: AttackChoiceIntent) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    attack = await self.convert(app.converters.AttackConverter, interaction, attack_query, arts=guild.arts, attacks=guild._attacks)
    if attack.intents.has_intent(intent.value):
      raise app.errors.AppError("attackAlreadyHasIntent")
    new_intents = attack.intents.copy()
    new_intents.set(intent.value)
    await attack.update(intents=new_intents)
    builder = app.embeds.AttackUpdatedBuilder(attack)
    await self.send_embed(interaction, builder, resolve_all=True)
  @apc.command(
    name="attack-reset-intents",
    description="[RPG Utilitários] Volta as intenções de um ataque para padrão."
  )
  @apc.guild_only()
  @apc.rename(attack_query="attack")
  async def attack_reset_intents(self, interaction: Interaction, /, *, attack_query: str) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    attack = await self.convert(app.converters.AttackConverter, interaction, attack_query, arts=guild.arts, attacks=guild._attacks)
    if attack.intents.is_empty():
      raise app.errors.AppError("attackIntentsIsEmpty")
    await attack.update(intents=AttackIntents())
    builder = app.embeds.AttackUpdatedBuilder(attack)
    await self.send_embed(interaction, builder, resolve_all=True)