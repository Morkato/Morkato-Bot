from __future__ import annotations

from typing import (
  Optional,
  Tuple,
  
  TYPE_CHECKING,
  Dict,
  Any
)

if TYPE_CHECKING:
  from .client import Morkato

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
  async def from_client(cls, client: Morkato, *, gateway: Optional[yarl.URL] = None) -> MorkatoWebSocket:
    gateway = gateway or client.DEFAULT_GATEWAY
    
    socket = await client.ws(gateway=gateway)
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