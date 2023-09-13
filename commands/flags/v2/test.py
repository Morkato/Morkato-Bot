from morkato.utils.flag import FlagGroup, flag

class TestGroup(FlagGroup):
  @flag(aliases=['c'])
  async def create(self, ctx) -> None:
    await ctx.send('Ok, o novo sistema v2 das flags funcionou!')