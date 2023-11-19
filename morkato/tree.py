from __future__ import annotations

from typing import TYPE_CHECKING

from discord import app_commands

import discord

if TYPE_CHECKING:
  from .client import MorkatoBot

__all__ = ('Tree',)

class Tree(discord.app_commands.CommandTree):
  async def on_error(self, interaction: discord.Interaction[MorkatoBot], error: discord.app_commands.errors.AppCommandError) -> None:
    if isinstance(error, app_commands.errors.CommandInvokeError):
      error = error.original

    msg = str(error if not hasattr(error, 'message') else error.message)

    try:
      await interaction.edit_original_response(content=f'`[{type(error).__name__}: Erro interno, desculpe-me] {msg}`')

    except app_commands.errors.AppCommandError:
      await interaction.response.send_message(f'Desculpe-me um erro insperado. Comunique a um desenvolvedor, tipo `{type(error).__name__}`, novamente, desculpe-me.')