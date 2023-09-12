from typing import Any, Callable, Coroutine, Optional

from discord.ext import commands

from morkato.client import MorkatoBot

from discord.ext.commands._types import Coro, Hook
from discord.ext.commands.context import Context

import datetime

class CommandV2(commands.Command):
  def __init__(self, func: Callable[..., Coro], /, **kwargs: Any) -> None:
    kwargs['name'] = 'command-v2-' + kwargs['name']

    super().__init__(func, **kwargs)

  async def invoke(self, ctx: Context[MorkatoBot]) -> Coroutine[Any, Any, None]:

    message = f"""```md
Command Invoked: {self.name}
Invoked for: {ctx.author.name}
Response Ten: True
Signature: {self.signature}
```"""
    
    return await super().invoke(ctx)