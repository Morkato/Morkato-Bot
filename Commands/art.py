from typing import Optional

import requests
from discord.ext import commands
from decouple import config

class Art(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  @commands.command(aliases=['Arte'])
  async def Art(self, ctx: commands.Context, /, *, art_name: Optional[str] = None) -> None:
    guild = getGuild(ctx.guild)

    if art_name and not art_name.lower() in ['respiration', 'kekkijutsu', 'attack']:
      art = guild.get_art(art_name)

      if art is None:
        await ctx.send('Essa arte não existe.')

        return
      
      for embed in art.embeds:
        await ctx.send(embed=embed)
      
      return
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Art(bot))