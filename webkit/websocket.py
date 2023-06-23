from typing import Callable, Union, Tuple, Dict, Any

from .http import HTTPClient

import aiohttp
import asyncio

import json

class WebSocket:
  def __init__(
    self,
    ws: aiohttp.ClientWebSocketResponse,
    loop: asyncio.AbstractEventLoop
  ) -> None:
    self.ws = ws
    self.loop = loop

    self.events = {}
  
  @classmethod
  async def from_http(cls, http: HTTPClient, url: str) -> "WebSocket":
    ws = await http.ws(url)
    loop = http.loop

    return cls(ws, loop)
  
  def _parse_message(self, message: str) -> Tuple[str, str | None]:
    try:
      data = json.loads(message)
      event_name = data.get('e')
      
      if event_name:
        return event_name, data.get('d')
      else:
        return None, None
    except json.JSONDecodeError:
      return None, None

  async def _handle_event(self, e: str, d: Any) -> None:
    try:
      await self.events[e](d)
    except:
      pass

  @property
  def closed(self) -> bool:
    return self.ws.closed
  
  def on(self, event: str):
    def decorator(func: Callable[[Any], None]) -> None:
      self.events[event] = func
    
    return decorator
  
  async def poll_events(self) -> None:
    async def receive_messages():
      while 1:
        msg = await self.ws.receive()

        if msg.type == aiohttp.WSMsgType.TEXT:
          event_name, data = self._parse_message(msg.data)
          await self._handle_event(event_name, data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
          print('WebSocket connection closed with exception:', self.ws.exception())
          break

    async def start():
      await receive_messages()

    task = asyncio.create_task(start())

    try:
      await task
    except asyncio.CancelledError:
      print('WebSocket connection was cancelled.')
    finally:
      await self.close()
    
  async def send(self, data: Union[Dict[str, Any], str, bytes]) -> None:
    if isinstance(data, dict):
      return await self.ws.send_str(json.dumps(data))
    elif isinstance(data, str):
      return await self.ws.send_str(data)
    elif isinstance(data, bytes):
      return await self.ws.send_bytes(data)
  
  async def close(self) -> None:
    await self.ws.close()