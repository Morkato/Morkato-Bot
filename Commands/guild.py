from discord.ext import commands
from utils import getGuild

class Guild(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Guild(bot))