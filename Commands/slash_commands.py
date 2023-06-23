from typing import List

from discord.ext import commands
from discord import app_commands
import discord

class SlashCommands(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @app_commands.command(name='ping', description="Mostra o ping atual do bot")
  async def ping(self, interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f'Pong! `{round(self.bot.latency*100, 2)}ms`')

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(SlashCommands(bot))