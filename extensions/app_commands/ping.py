from discord import app_commands

from morkato.client import MorkatoBot, Cog

import discord

class Ping(Cog):
  @app_commands.command(name='ping', description='[Utilitários] Mostra meu ping atual 🏓')
  async def ping(self, interaction: discord.Interaction) -> None:
    latency_discord = round(self.bot.latency * 100, 2)
    latency_morkato = round(self.bot.ws_morkato.latency * 100, 2)
    
    ping = f"🏓| Discord: **`{latency_discord}ms`**\n🏓| Morkato: **`{latency_morkato}ms`**\n🏓| Pong!"
    
    if interaction.is_expired():
      await interaction.response.defer()

    await interaction.response.send_message(ping)

async def setup(bot: MorkatoBot) -> None:
  await bot.add_cog(Ping(bot))
