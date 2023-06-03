from typing import Optional

from discord.ext import commands
from utils import getGuild

class Art(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  @commands.command(aliases=['Arte'])
  async def Art(self, ctx: commands.Context, /, *, art_name: Optional[str] = None) -> None:
    guild = getGuild(ctx.guild)

    if art_name:
      art = guild.get_art(art_name)

      if art is None:
        await ctx.send('Essa arte não existe.')

        return

      for embed in art.embeds:
        await ctx.send(embed=embed)
      
      return
  @commands.command(name='attacks')
  async def Attack(self, ctx: commands.Context, /) -> None:
    guild = getGuild(ctx.guild)

    await ctx.send(f'`{guild.attacks}`')
  
  @commands.command(name='new-resp')
  async def New_Respiration(self, ctx: commands.Context, /, *, name: str) -> None:
    guild = getGuild(ctx.guild)

    resp = guild.new_respiration(name)

    await ctx.send(f'**Uma nova respiração chamada: `{resp.name}` foi criada!**')

  @commands.command(name='edit-resp')
  async def Edit_Respiration(self, ctx: commands.Context, /, *, name: str) -> None: ...
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Art(bot))