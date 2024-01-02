from __future__ import annotations

from typing import (
  Coroutine,
  Callable,
  Optional,
  Dict,
  Union,
  Final,

  TYPE_CHECKING,
  Any
)

if TYPE_CHECKING:
  from typing_extensions import Self

  from .bot import MorkatoBotBase

from datetime import datetime

import logging
import asyncio
import aiohttp
import zlib
import orjson
import yarl
import os

class WebSocketError(Exception): ...
class WebSocketClosure(WebSocketError): ...

logger = logging.getLogger(__name__)

class MorkatoWebSocket:
  DEFAULT_GATEWAY: Final[yarl.URL] = yarl.URL(os.getenv('MORKATO_GATEWAY', "ws://localhost:5550"))

  DISPATCH  = 0
  HEARTBEAT = 1
  IDENTIFY  = 2
  READY     = 3
  HELLO     = 4

  @classmethod
  async def from_client(
    cls,
    bot: MorkatoBotBase, *,
    gateway: Optional[yarl.URL] = None
  ) -> Self:
    http = bot.morkato_http
    state = bot._morkato_connection
    loop = bot.loop
    
    gateway = gateway or cls.DEFAULT_GATEWAY

    socket = await http.ws_connect(str(gateway))

    ws = cls(socket, loop=loop)

    ws.gateway = gateway
    ws.authorization = http.token
    ws._dispatch = state.dispatch
    ws._parsers = state.parsers

    await ws.identify()

    logger.info("Foi conectado com sucesso ao websocket (Origem: Gateway).")

    return ws

  def __init__(self, socket: aiohttp.ClientWebSocketResponse, *, loop: asyncio.AbstractEventLoop) -> None:
    self.socket = socket
    self.loop = loop

    self.gateway: yarl.URL = None # type: ignore
    self.authorization: str = None # type: ignore
    self._dispatch: Callable[..., Coroutine[Any, Any, None]] = lambda *args: None

    self._buffer = bytearray()
    self._zlib = zlib.decompressobj()

    self._parsers: Dict[str, Callable[..., Any]] = {  }

  async def identify(self) -> None:
    cls = self.__class__

    payload = {
      'op': cls.IDENTIFY,
      'd': {
        'authorization': self.authorization
      }
    }

    await self.socket.send_json(payload)

  async def received_message(self, msg: Union[str, bytes]) -> None:
    if isinstance(msg, bytes):
      self._buffer.extend(msg)

      if len(msg) < 4 or msg[-4:] != b'\x00\x00\xff\xff':
        return
      
      msg = self._zlib.decompress(self._buffer)
      msg = msg.decode('utf-8')

    if not isinstance(msg, str):
      return
    
    recv = orjson.loads(msg)

    if not isinstance(recv, dict):
      raise RuntimeError
    
    cls = self.__class__

    op = recv.get('op')
    e  = recv.get('e')
    d  = recv.get('d')

    if op == cls.DISPATCH and e:
      parser = self._parsers.get(e)

      if not parser:
        logger.warn('Unknown dispatch: %s', e)

        return
      
      parser(d)

    elif op == cls.HEARTBEAT:
      await self.socket.send_json({
        "op": cls.HEARTBEAT,
        'd': datetime.now().timestamp() * 1000
      })
  
  async def poll_event(self) -> None:
    recv = await self.socket.receive()
    
    if recv.type in (aiohttp.WSMsgType.TEXT, aiohttp.WSMsgType.BINARY):
      return await self.received_message(recv.data)
      
    elif recv.type == aiohttp.WSMsgType.ERROR:
      raise recv.data
      
    elif recv.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSE):
      raise WebSocketClosure(recv.type)