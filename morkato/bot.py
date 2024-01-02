from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  overload,
  Optional,
  Sequence,
  Union,
  Type,
  List,
  Any
)

from discord.message import Message

if TYPE_CHECKING:
  from typing_extensions import Self

  from .abc import Snowflake
  from .types._etc import AppBotContextT
  from discord.message import Message

  from .guild import Guild

  from re import Pattern

from discord.ext.commands.errors import CommandInvokeError
from discord.ext.commands.bot import Bot
from discord.flags import Intents

from .gateway import MorkatoWebSocket, WebSocketClosure
from .context import MorkatoContext, AppBotContext
from .state import MorkatoConnectionState
from .errors import ErrorType, geterr
from .errors import BaseError
from .backoff import Backoff
from .http import HTTPClient

from glob import glob

import discord
import logging
import asyncio
import aiohttp
import os

logger = logging.getLogger(__name__)

class BotApp(Bot):
  def __init__(self, prefix: List[str], *, dev: Optional[Pattern] = None, intents: Intents, **options: Any) -> None:
    super().__init__(prefix, intents=intents, **options)

    self._dev = dev

  async def on_ready(self) -> None:
    await self.tree.sync()

    await self.change_presence(activity = discord.Game("Pudim. O Game (LTS)"), status = discord.Status.dnd)

    logger.info("Estou conectado, como: %s", self.user)
  
  @overload
  async def get_context(self, origin: Message, /) -> AppBotContext: ...
  @overload
  async def get_context(self, origin: Message, /, *, cls: Type[AppBotContextT]) -> AppBotContextT: ...
  async def get_context(self, origin: Message, /, *, cls: Optional[Type[AppBotContextT]] = None) -> Union[AppBotContext, AppBotContextT]:
    if cls is not None and not issubclass(cls, AppBotContext):
      raise RuntimeError

    return await super().get_context(origin, cls=cls or AppBotContext)
  
  async def on_command_error(self, ctx: AppBotContext[BotApp], err: Exception) -> None:
    if not isinstance(err, CommandInvokeError):
      logger.error("Ignoring exception %s", err)

      raise err

    error = err.original

    if not isinstance(error, BaseError):
      await ctx.send(f'`[{type(error).__name__} - generic.unknown: Error!] {error}`')

      logger.error("Ignoring error: %s", error)

      raise err
    
    message = error.get_discord_message()
    
    if ctx.isDev:
      default_message = BaseError.get_discord_message(error)

      await ctx.send('Default (LOG): %s\nMessage (%s): %s' % (default_message, type(error).__name__, message))

      return

    await ctx.send(message)

  async def setup_hook(self) -> None:
    app = 'app'
    
    extensions = glob(os.path.join(app, 'extensions/*.py')) +  glob(os.path.join(app, 'extensions/**/**.py'))
    
    for ext in extensions:
      ext = ext.replace('/', '.')
      ext = ext[:-3]

      logger.info("Loading Extension: %s", ext)

      await self.load_extension(ext)

class MorkatoBotBase(BotApp):
  def __init__(self, prefix: List[str], token: str, dev: Optional[Pattern] = None, **options: Any) -> None:
    super().__init__(prefix, dev=dev, intents=Intents.all(), **options)

    self.morkato_http = HTTPClient()
    
    self._morkato_connection = self.get_morkato_state()
    self._morkato_ws: MorkatoWebSocket = None # type: ignore

    self._morkato_token = token
  
  async def get_context(self, origin: Message) -> MorkatoContext[Self]:
    return await super().get_context(origin, cls=MorkatoContext)
  
  def get_morkato_state(self) -> MorkatoConnectionState:
    return MorkatoConnectionState(dispatch=self.morkato_dispatch, http=self.morkato_http)
  
  def get_morkato_guild(self, obj: Snowflake) -> Guild:
    guild = self._morkato_connection._get_guild(obj.id)

    if not guild:
      raise geterr(ErrorType.GUILD_NOTFOUND)
    
    return guild
  
  def get_morkato_websocket(self) -> MorkatoWebSocket:
    if not self._morkato_ws:
      raise RuntimeError
    
    return self._morkato_ws
  
  async def login(self, token: str) -> None:
    http = self.morkato_http
    await asyncio.gather(super().login(token), http.login(self._morkato_token))

  async def connect(self, *, reconnect: bool = True) -> None:
    await asyncio.gather(super().connect(reconnect=reconnect), self.morkato_connect(reconnect=reconnect))

  async def close(self) -> None:
    if self.morkato_http:
      await self.morkato_http.close()

    await super().close()
  
  async def morkato_connect(self, *, reconnect: bool = True) -> None:
    backoff = Backoff()

    while not self.is_closed():
      try:
        self._morkato_ws = await MorkatoWebSocket.from_client(self)

        while True:
          await self._morkato_ws.poll_event()
      except (aiohttp.ClientConnectorError, WebSocketClosure):
        self._morkato_ws = None # type: ignore

        wait = round((backoff.delay() + 6) / 5) * 5

        logger.warn("Não foi possível conectar ao websocket, tentando nova conexão em: %ss", wait)
        await asyncio.sleep(wait)
        
        continue
      except asyncio.CancelledError:
        self._morkato_ws = None # type: ignore

        logger.info("Fechando WebSocket.")

        return
  
  def morkato_dispatch(self, event: str, *args) -> None: ...

class MorkatoBot(MorkatoBotBase): ...