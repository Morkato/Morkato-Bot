from .groups.art import ArtGroupFlags

from morkato.converters import CommandConverter
from morkato            import (
  MorkatoContext,
  MorkatoBot,
  Cog,

  utils
)

from discord.ext import commands

class Art(Cog):
  GROUP: ArtGroupFlags

  @commands.command(name='art')
  async def art(self, ctx: MorkatoContext, *, cmd: CommandConverter) -> None:
    ctx.debug_counter()
    
    if cmd.params:
      await utils.process_flags(Art.GROUP, ctx=ctx, base=cmd.base, params=cmd.params)

      return
    
    if not cmd.base:
      await ctx.send('Tá, mas qual é o nome?')

      return
      
    art = self.get_art(ctx.guild, cmd.base)

    ctx.debug_counter()    

    await ctx.send_art(art)
    
async def setup(bot: MorkatoBot) -> None:
  cog = Art(bot)

  Art.GROUP = ArtGroupFlags(cog)
  
  await bot.add_cog(cog)
