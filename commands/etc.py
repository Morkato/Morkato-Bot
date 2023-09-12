from .ext import Command, command_by_flag, flag

from discord.ext   import commands
from morkato.objects.guild import Guild

from morkato import Cog

class Test(Command):
  @flag(name='def', aliases=['default'])
  async def default(self, ctx: commands.Context, guild: Guild) -> None:
    await ctx.send('Essa é a flag default (y)')

  @flag(name='c')
  async def ju(self, ctx: commands.Context, guild: Guild) -> None:
    await ctx.send('Essa é a flag "c" (y)')

test = Test()

class Etc(Cog):
  @commands.command('test-c')
  async def test_t(self, ctx: commands.Context, *, text: str) -> None:
    await command_by_flag(command=test, db=self.db, ctx=ctx, text=text)

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Etc(bot))