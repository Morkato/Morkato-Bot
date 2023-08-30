from .ext import command_by_flag

from morkato.client import MorkatoBot, Cog
from discord.ext    import commands

from .flags.attack import AttackCommand
from .flags.art    import ArtCommand

class Art(Cog):
  def __init__(self, bot: MorkatoBot) -> None:
    super().__init__(bot)

    self.attack_command = AttackCommand(case_insensitive=True)
    self.art_command    = ArtCommand(case_insensitive=True)
  
  @commands.command(name='art')
  async def Art(self, ctx: commands.Context, /, *, text: str) -> None:
    return await command_by_flag(command=self.art_command, client=self.bot, ctx=ctx, text=text)
  
  @commands.command(aliases=['a', 'atk'])
  async def Attack(self, ctx: commands.Context, /, *, text: str) -> None:
    return await command_by_flag(command=self.attack_command, client=self.bot, ctx=ctx, util=(ctx.author), text=text)
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Art(bot))
