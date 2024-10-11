from morkato.work.project import registry
from app.extension import BaseExtension
from discord import app_commands as apc
from discord import (Interaction, User)
from typing import Optional
import app.errors
import app.embeds

@registry
class RPGPlayer(BaseExtension):
  LANGUAGE: str
  async def setup(self) -> None:
    self.LANGUAGE = self.builder.PT_BR
  @apc.command(
    name="pregister",
    description="[RPG Utilitários] Registra um jogador"
  )
  @apc.guild_only()
  async def player_register(
    self, interaction: Interaction, *,
    user: User,
    name: str,
    surname: str,
    icon: Optional[str]
  ) -> None:
    if not interaction.user.guild_permissions.manage_guild:
      user = interaction.user
    guild = await self.get_morkato_guild(interaction.guild)
    player = await self.get_cached_or_fetch_player(guild, user.id)
    if player.already_registered():
      raise app.errors.AppError("onPlayerAlreadyRegistered")
    await interaction.response.defer()
    npc = await player.registry(name, surname, icon=icon)
    embed = await app.embeds.NpcCardBuilder(npc).build(0)
    await interaction.edit_original_response(embed=embed)