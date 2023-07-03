from .attack_utils import get as getAttackFlag
from .art_utils    import get as getArtFlag

from utils.guild    import Guild, get as getGuild
from utils.string   import Context, parse_params
from utils.commands import command_by_flag

from discord.ext import commands

class Art(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  @commands.command(aliases=['Arte'])
  async def Art(self, ctx: commands.Context, /, *, text: str) -> None:
    return await command_by_flag(flag_gether=getArtFlag, ctx=ctx, text=text)

  @commands.command(name='attacks')
  async def Attack(self, ctx: commands.Context, /) -> None:
    guild = getGuild(ctx.guild)

    await ctx.send(f'`{guild.attacks}`')
  
  @commands.command(aliases=['a', 'ataque'])
  async def Attack(self, ctx: commands.Context, /, *, text: str) -> None:
    return await command_by_flag(flag_gether=getAttackFlag, ctx=ctx, text=text)
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Art(bot))
