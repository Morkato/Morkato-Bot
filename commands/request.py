from morkato.client import Cog
from discord.ext    import commands

from webkit import (
  Response,
  Request,
  request,
)

import orjson

class RequestCommand(Cog):
  @commands.command(name='request')
  async def request(self, ctx: commands.Context, method: str, *, route: str) -> None:
    async def resolver(res: Response) -> tuple[str, str]:
      type = res.headers.get('content-type')
      
      return (type, await res.content())

    content_type, content = await request(Request(method, route, headers={ 'authorization': self.bot.auth }), call=resolver)

    if content_type == 'application/json; charset=utf-8':
      await ctx.send(f'```json\n{content}```')

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(RequestCommand(bot))