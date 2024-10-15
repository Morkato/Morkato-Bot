from morkato.work.extension import command
from morkato.work.project import registry
from morkato.types import ArtType
from discord.interactions import Interaction
from app.extension import BaseExtension
from discord import app_commands as apc
from typing import Optional
import app.embeds
import app.checks

@registry
class RPGArtsAttacksExtension(BaseExtension):
  LANGUAGE: str
  async def setup(self) -> None:
    self.has_guild_perms = app.checks.has_guild_permissions(manage_guild=True)
    self.LANGUAGE = self.builder.PT_BR
    self.art_create.add_check(self.has_guild_perms)
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