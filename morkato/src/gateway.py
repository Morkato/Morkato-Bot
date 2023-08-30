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

class WebSocketClosure(Exception):
  pass

class MorkatoWebSocket:  
  def __init__(
      self,
      socket:  aiohttp.ClientWebSocketResponse, *,
      loop:    asyncio.AbstractEventLoop,
    ) -> None:
    self.socket = socket
    self.loop   = loop
  
  @classmethod
  async def from_session(cls, session: MorkatoSessionController, *, gateway: yarl.URL) -> MorkatoWebSocket:
    socket = await session.ws(gateway=gateway)
    loop   = asyncio.get_running_loop()

    return cls(socket, loop=loop)
  
  def _handle_context(self, data: Dict[str, Any]) -> Tuple[str, Any]:
    return data['e'], data['d']
  
  async def received_message(self, msg: Any, /) -> Tuple[str, Any]:
    if type(msg) is bytes:
      msg = msg.decode('utf-8')

    msg = orjson.loads(msg)

    event, data = self._handle_context(msg)

    return event, data

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
      return None, None
  
  async def close(self) -> bool:
    return await self.socket.close()
  

class MorkatoWebSocketManager:
  DEFAULT_GATEWAY = yarl.URL(getEnv('GATEWAY', 'ws://localhost:80'))

  def __init__(self, gateway: MorkatoWebSocket) -> None:
    self.__gateway = gateway
  
  @classmethod
  async def from_session(cls, session: MorkatoSessionController, *, gateway: Optional[yarl.URL] = None) -> MorkatoWebSocket:
    gateway = gateway or cls.DEFAULT_GATEWAY
    
    return await MorkatoWebSocket.from_session(session, gateway=gateway)

  def get_event(self, event: str) -> Union[Callable[[MorkatoClientManager, Any], Coroutine[Any, Any, None]], None]:
    call = next((callback for event_name, callback in events if event_name == event), None)

    if not call:
      return
    
    return call

  async def pool_event(self, timeout: Optional[float] = None) -> Tuple[str, Any]:
    return await self.__gateway.pool_event(timeout)
  
  async def close(self) -> bool:
    return await self.close()