from morkbmt.extension import ExtensionCommandBuilder
from morkbmt.core import registry
from morkato.errors import PlayerNotFoundError
from app.extension import BaseExtension
from discord import app_commands as apc
from discord import (Interaction, User)
from typing_extensions import Self
from typing import (Optional, ClassVar)
import discord.ext.commands
import app.errors
import app.embeds

@registry
class RPGPlayer(BaseExtension):
  LANGUAGE: ClassVar[str]
  async def setup(self, commands: ExtensionCommandBuilder[Self]) -> None:
    self.LANGUAGE = self.msgbuilder.PT_BR
    self.manage_guild_perms = discord.ext.commands.has_guild_permissions(manage_guild=True)
    self.check(self.player_registry, self.manage_guild_perms)
    self.check(self.player_reset, self.manage_guild_perms)
  @apc.command(
    name="pregistry",
    description="[RPG Utilitários] Registra um jogador"
  )
  @apc.guild_only()
  async def player_registry(
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
      raise app.errors.AppError("playerAlreadyRegistered")
    await interaction.response.defer()
    npc = await player.registry(name, surname, icon=icon)
    builder = app.embeds.NpcCardBuilder(npc)
    await self.send_embed(interaction, builder, resolve_all=True)
  @apc.command(
    name="preset",
    description="[RPG Utilitários] Excluí o contexto para um jogador"
  )
  @apc.guild_only()
  async def player_reset(self, interaction: Interaction, user: User) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    try:
      player = await self.get_cached_or_fetch_player(guild, user.id)
      await player.delete()
      content = self.get_content(self.LANGUAGE, "playerReset", user=user)
      await interaction.edit_original_response(content=content)
    except PlayerNotFoundError:
      raise app.errors.AppError("invalidPlayerContext")