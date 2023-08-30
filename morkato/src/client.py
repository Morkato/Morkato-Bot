from __future__ import annotations

from typing import (
  NoReturn,
  
  Any
)

from .session  import MorkatoSessionController
from .database import MorkatoDatabaseManager
from .gateway  import MorkatoWebSocketManager

from discord.ext import commands
from discord     import Intents

from errors    import BaseError
from glob      import glob

import asyncio
import re

class MorkatoClientManager(commands.Bot):
  def __init__(self, auth: str, command_prefix: str = '!', case_insensitive: bool = True) -> None:
    super(commands.Bot, self).__init__(
      command_prefix=command_prefix,
      intents=Intents.all(),
      case_insensitive=case_insensitive
    )

    self.__api:      MorkatoSessionController = None # type: ignore
    self.__database: MorkatoDatabaseManager   = None # type: ignore
    self.__gateway:  MorkatoWebSocketManager  = None # type: ignore

    self.__auth = auth
  
  async def __aexit__(self, *args, **kwargs) -> None:
    print('Ih, fechou')

    self.__gateway_pool_events_task.cancel()
    
    await self.__gateway.close()
    await self.__api.close()
    
    await super().__aexit__(*args, **kwargs)

  async def handle_event(self, e: str, d: Any) -> None:
    event = self.__gateway.get_event(e)

    if not event:
      return
    
    return await event(self, d)

  async def start(self, token: str, *, reconnect: bool = True) -> None:
    api      = await MorkatoSessionController(auth=self.__auth).start()
    gateway  = await MorkatoWebSocketManager.from_session(api)
    database = await MorkatoDatabaseManager.from_gateway(self, gateway)

    self.__api      = api
    self.__gateway  = gateway
    self.__database = database

    async def pool_events() -> NoReturn:
      while True:
        (event, data) = await gateway.pool_event()

        await self.handle_event(event, data)
      
    task = asyncio.create_task(pool_events())

    self.__gateway_pool_events_task = task

    return await super().start(token, reconnect=reconnect)
  
  @property
  def api(self) -> MorkatoSessionController:
    return self.__api
  
  @property
  def gateway(self) -> MorkatoWebSocketManager:
    return self.__gateway

  @property
  def database(self) -> MorkatoDatabaseManager:
    return self.__database
  
  async def on_ready(self) -> None:
    await self.tree.sync()
    
    print(f'Estou conectado, como : {self.user}')

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

class MorkatoBot(MorkatoClientManager):
  """
    doc
  """

  pass

class Cog(commands.Cog):
  def __init__(self, bot: MorkatoBot) -> None:
    self.bot = bot

    self.database = bot.database
    self.gateway  = bot.gateway
    self.api      = bot.api
