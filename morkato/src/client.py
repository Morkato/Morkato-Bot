from __future__ import annotations

from typing import (
  Optional,
  Tuple,
  
  Any
)

from .session import MorkatoSessionController
from .gateway import MorkatoWebSocket
from .events  import events

from discord.ext import commands
from discord     import Intents

from errors  import BaseError
from objects import (
  Attacks,
  Guilds,
  Arts
)

from utils.etc import getEnv
from glob      import glob

import aiohttp
import yarl
import re

class Morkato(MorkatoSessionController):
  DEFAULT_GATEWAY = yarl.URL(getEnv('GATEWAY', 'ws://localhost:80'))

  def __init__(self, auth: str) -> None:
    super().__init__(auth=auth)
    
    self.attacks = Attacks()
    self.guilds  = Guilds([])
    self.arts    = Arts()
    
    
    self.gateway: MorkatoWebSocket = None # type: ignore

  async def start(self, *, gateway: Optional[yarl.URL] = None) -> Morkato:
    await super().start()

    gateway = gateway or self.DEFAULT_GATEWAY
    
    self.gateway = await MorkatoWebSocket.from_client(self, gateway=gateway)

    return self
  
  async def handle_events(self, event: str, data: Any) -> None:
    call = next((callback for event_name, callback in events if event_name == event), None)

    if not call:
      return
    
    await call(self, data)

  async def pool_event(self, timeout: Optional[float] = None) -> Tuple[str, Any]:
    return await self.gateway.pool_event(timeout)
  
  async def ws(self, *, gateway: Optional[yarl.URL] = None) -> aiohttp.ClientWebSocketResponse:
    gateway = gateway or self.DEFAULT_GATEWAY
    
    return await self.session.ws(str(gateway))
  
  async def close(self) -> bool:
    return (await super().close()) and (await self.gateway.close())

class Client(commands.Bot):
  def __init__(self, auth: str, command_prefix: str = '!', case_insensitive: bool = True) -> None:
    super(commands.Bot, self).__init__(
      command_prefix=command_prefix,
      intents=Intents.all(),
      case_insensitive=case_insensitive
    )

    self.conn = Morkato(auth=auth)
  
  async def __aexit__(self, *args, **kwargs) -> None:
    print('Ih, fechou')

    await self.conn.close()

    await super().__aexit__(*args, **kwargs)

  async def start(self, token: str, *, reconnect: bool = True) -> None:
    await self.conn.start()
    
    return await super().start(token, reconnect=reconnect)
  
  async def on_ready(self) -> None:
    await self.tree.sync()
    
    print(f'Estou conectado, como : {self.user}')
    
    while True:
      event, data = await self.conn.pool_event()

      await self.conn.handle_events(event, data)
  
  async def on_command_error(self, ctx: commands.Context, err: Exception) -> None:
    if not isinstance(err, commands.errors.CommandInvokeError):
      raise err

    error = err.original

    if not isinstance(error, BaseError):
      await ctx.send(f'Desculpe-me um erro insperado. Comunique a um desenvolvedor, tipo `{type(error).__name__}`, novamente, desculpe-me.')

      raise error
    
    await ctx.send(error.message)
  
  async def setup_hook(self) -> None:
    for file in glob('commands/*.py'):
      if re.match(r'commands/(ext|flags)/.*', file):
        continue

      if file[-3:] == '.py':
        await self.load_extension(file[:-3].replace('/', '.'))

class Cog(commands.Cog):
  def __init__(self, bot: Client) -> None:
    self.bot = bot

    self.db = bot.conn
