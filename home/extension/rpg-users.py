from morkbmt.extension import (ExtensionCommandBuilder, Converter)
from morkbmt.bot import MorkatoBot
from morkbmt.core import registry
from morkato.errors import UserNotFoundError
from discord.interactions import Interaction
from app.extension import BaseExtension
from typing_extensions import Self
import app.errors
import discord.ext.commands
import discord

@registry
class RPGUsersExtension(BaseExtension):
  async def setup(self, commands: ExtensionCommandBuilder[Self]) -> None:
    self.LANGUAGE = self.msgbuilder.PT_BR
    self.manage_guild_perms = discord.ext.commands.has_guild_permissions(manage_guild=True)
    user_reset = commands.app_command("user-reset", self.user_reset, description="[RPG Utilitários] Excluí o registro do usuário requisitado.")
    commands.guild_only(user_reset)
    commands.rename(user_reset, dis_user="user")
    commands.check(user_reset, self.manage_guild_perms)
  async def user_reset(self, interaction: Interaction[MorkatoBot], /, dis_user: discord.User) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    user = guild.get_cached_user(dis_user)
    try:
      user = await guild.fetch_user(dis_user.id)
    except UserNotFoundError:
      raise app.errors.AppError("userNotRegistered", user=dis_user)
    await user.delete()
    content = self.msgbuilder.get_content(self.LANGUAGE, "userToUnregistered", user=dis_user)
    await interaction.edit_original_response(content=content)