from __future__ import annotations

from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
  from ..context import MorkatoContext

import time

class LoggerCommand(commands.Command):
  async def invoke(self, ctx: MorkatoContext) -> None:
    before = time.time()

    await super().invoke(ctx)

    after = time.time() - before

    await ctx.send(f'Response time: **`{round(after * 100, 2)}ms`**')