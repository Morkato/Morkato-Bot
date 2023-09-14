from .v2.art import ArtGroupFlags

from morkato.converters import CommandConverter
from morkato            import (
  MorkatoContext,
  MorkatoBot,
  Cog,

  utils
)

from discord.ext import commands

class Art(Cog):
  GROUP: ArtGroupFlags = ArtGroupFlags()

  @commands.command(name='art', cls=utils.LoggerCommand)
  async def art(self, ctx: MorkatoContext, *, cmd: CommandConverter) -> None:
    guild = ctx.morkato_guild
    
    if not cmd.params:
      if not cmd.base:
        await ctx.send('Tá, mas qual é o nome?')

        return
      
      arts = guild.get_arts_by_name(cmd.base)

      art = arts[0]

      await ctx.send_art(art)
      
      return
    
    await utils.process_flags(Art.GROUP, ctx=ctx, base=cmd.base, params=cmd.params)
    
async def setup(bot: MorkatoBot) -> None:
  await bot.add_cog(Art(bot))
