from typing_extensions import Self
from .errors import (HTTPException, NotFoundError, MorkatoServerError)
from urllib.parse import quote
from typing import (
  Optional,
  ClassVar,
  Union,
  Dict,
  Any
)

import logging
import asyncio
import aiohttp
import orjson
import sys
import os

logger = logging.getLogger(__name__)

async def json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
  text = await response.text(encoding='utf-8')
  try:
    type = response.headers['Content-Type'].split(';', 1)[0]
    if type == 'application/json':
      return orjson.loads(text)
  except KeyError:
    pass
  return text

class Route:
  BASE: ClassVar[str] = os.getenv("URL", "http://localhost:5500")
  def __init__(self, method: str, path: str, **parameters):
    self.path: str = path
    self.method: str = method
    url = self.BASE + self.path
    
    if parameters:
      url = url.format_map({k: quote(v) if isinstance(v, str) else v for k, v in parameters.items()})
    
    self.url: str = url

class HTTPClient:
  def __init__(
    self,
    loop: Optional[asyncio.AbstractEventLoop] = None,
    connector: Optional[aiohttp.BaseConnector] = None
  ) -> None:
    self.loop = loop
    self.connector = connector
    self.__session: aiohttp.ClientSession = None # type: ignore
    user_agent = 'morkato (https://github.com/morkato/morkato-Bot {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
    self.user_agent: str = user_agent.format(1.0, sys.version_info, aiohttp.__version__)
  async def __aenter__(self) -> Self:
    return self
  async def __aexit__(self, *args) -> None:
    await self.close()
  async def ws_connect(self, url: str) -> aiohttp.ClientWebSocketResponse:
    kwargs = {
      'max_msg_size': 0,
      'timeout': 30.0,
      'headers': {
          'User-Agent': self.user_agent
      },
      'autoping': False
    }
    return await self.__session.ws_connect(url, **kwargs)
  async def static_login(self) -> None:
    if self.loop == None:
      self.loop = asyncio.get_running_loop()
    if self.connector is None:
      self.connector = aiohttp.TCPConnector(limit=0)
    self.__session = aiohttp.ClientSession(
      connector=self.connector
    )
  async def close(self) -> None:
    if self.__session is not None:
      await self.__session.close()
      self.__session = None # type: ignore
  async def request(self, route: Route, **kwargs) -> Any:
    if not self.__session:
      raise NotImplementedError
    headers: Dict[str, Union[str, int]] = {
      "User-Agent": self.user_agent
    }
    if "json" in kwargs:
      headers["Content-Type"] = "application/json; charset=utf-8"
      kwargs["data"] = orjson.dumps(kwargs.pop("json"))
    kwargs["headers"] = headers
    method = route.method
    url = route.url
    for tries in range(5):
      try:
        async with self.__session.request(method, url, **kwargs) as response:
          status = response.status
          data = await json_or_text(response)
          logger.debug("%s %s retornou: %s", method, url, status)
          if not status in range(200, 300):
            message = data.get("message")
            if status == 404:
              raise NotFoundError(response, message)
            elif status >= 500:
              raise MorkatoServerError(response, message)
            raise HTTPException(response, message)
          return data
      except OSError as err:
        if tries < 4 and err.errno in (54, 10054):
          await asyncio.sleep(1 + tries * 2)
          continue
        raise