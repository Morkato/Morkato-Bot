from __future__ import annotations

from typing import (
  Coroutine,
  Callable,
  Optional,
  Union,
  Tuple,
  
  TYPE_CHECKING,
  Dict,
  Any
)

if TYPE_CHECKING:
  from .session import MorkatoSessionController
  from .client  import MorkatoClientManager

from utils.etc import getEnv

from .events   import events

import aiohttp
import asyncio

import orjson
import yarl

import logging

_log = logging.getLogger(__name__)

class WebSocketClosure(Exception):
  pass

class MorkatoWebSocket:  
  def __init__(
      self,
      socket: aiohttp.ClientWebSocketResponse, *,
      loop:    Optional[asyncio.AbstractEventLoop] = None,
    ) -> None:
    self.socket = socket
    self.loop   = loop or asyncio.get_running_loop()
  
  @classmethod
  async def from_session(cls, session: MorkatoSessionController, *, gateway: yarl.URL) -> MorkatoWebSocket:
    socket = await session.ws(gateway=gateway)

    return cls(socket)

  def _handle_context(self, data: Dict[str, Any]) -> Tuple[str, Any]:
    return data['e'], data['d']
  
  async def received_message(self, msg: Any, /) -> Tuple[str, Any]:
    if type(msg) is bytes:
      msg = msg.decode('utf-8')

    msg = orjson.loads(msg)

    event, data = self._handle_context(msg)

    return event, data
  
  @property
  def closed(self) -> bool:
    return self.socket.closed
  
  async def pool_event(self, timeout: Optional[float] = None) -> Tuple[str, Any]:
    try:
      coro = self.socket.receive()

      msg = await coro

      if msg.type in (aiohttp.WSMsgType.TEXT, aiohttp.WSMsgType.BINARY):
        return await self.received_message(msg.data)
      
      elif msg.type == aiohttp.WSMsgType.ERROR:
        raise msg.data
      
      elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSE):
        raise WebSocketClosure
      
    except (asyncio.TimeoutError, WebSocketClosure) as err:
      raise

  async def close(self) -> bool:
    return await self.socket.close()
  

class MorkatoWebSocketManager:
  DEFAULT_GATEWAY = yarl.URL(getEnv('GATEWAY', 'ws://localhost:80'))

  def __init__(self, gateway: MorkatoWebSocket) -> None:
    self.__gateway = gateway
  
  @classmethod
  async def from_session(cls, session: MorkatoSessionController, *, gateway: Optional[yarl.URL] = None) -> MorkatoWebSocket:
    gateway = gateway or cls.DEFAULT_GATEWAY
    
    _log.info('Conectando com o gateway.')

    return MorkatoWebSocketManager(await MorkatoWebSocket.from_session(session, gateway=gateway))

  @property
  def closed(self) -> bool:
    return self.__gateway.closed
  
  def get_event(self, event_name: str) -> Union[Callable[[MorkatoClientManager, Any], Coroutine[Any, Any, None]], None]:
    call = next((event[1] for event in events if event[0] == event_name), None)

    if not call:
      return
    
    return call

  async def pool_event(self, timeout: Optional[float] = None) -> Tuple[str, Any]:
    return await self.__gateway.pool_event(timeout)
  
  async def close(self) -> bool:
    return await self.__gateway.close()