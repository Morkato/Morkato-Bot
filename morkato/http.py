from typing import (
  Optional,
  ClassVar,
  Iterable,
  Union,
  Dict,
  Any
)

from urllib.parse import quote

from .errors import geterr, ErrorType
from .utils.etc import in_range

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
  except KeyError: ...

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
    connector: Optional[aiohttp.BaseConnector] = None,
  ) -> None:
    self.loop = loop
    self.connector = connector
    self.token: Optional[str] = None

    self.__session: aiohttp.ClientSession = None # type: ignore

    user_agent = 'Morkato (https://github.com/Morkato/Morkato-Bot {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
    self.user_agent: str = user_agent.format(1.0, sys.version_info, aiohttp.__version__)

  def __repr__(self) -> str:
    return f'<{self.__class__.__name__} login={(self.token or "anonymous")}>'
  
  def clear(self) -> None:
    if self.__session and self.__session.closed:
      self.__session = None # type: ignore
  
  async def ws_connect(self, url: str, *, compress: int = 0) -> aiohttp.ClientWebSocketResponse:
    kwargs = {
      'max_msg_size': 0,
      'timeout': 30.0,
      'autoclose': False,
      'headers': {
          'User-Agent': self.user_agent,
      },
      'compress': compress,
    }

    return await self.__session.ws_connect(url, **kwargs)
  
  async def request(
    self,
    route: Route,
    *,
    form: Optional[Iterable[Dict[str, Any]]] = None,
    **kwargs: Any,
  ) -> Any:
    error = geterr(ErrorType.GENERIC, message="Você não está logado na sessão ativa.")

    if not self.token:
      raise error

    method = route.method
    url = route.url

    headers: Dict[str, str] = {
      "User-Agent": self.user_agent,
      "Authorization": self.token
    }

    if 'json' in kwargs:
      headers['Content-Type'] = "application/json"
      kwargs['data'] = orjson.dumps(kwargs.pop('json'))

    kwargs['headers'] = headers
    
    response: Optional[aiohttp.ClientResponse] = None
    data: Optional[Union[Dict[str, Any], str]] = None

    for tries in range(5):
      if form:
        form_data = aiohttp.FormData(quote_fields=False)

        for params in form:
          form_data.add_field(**params)
        kwargs['data'] = form_data
      
      try:
        async with self.__session.request(method, url, **kwargs) as response:
          status = response.status
          
          logger.info("%s %s retornou: %s", method, url, status)

          data = await json_or_text(response)

          if in_range(status, (200, 299)):
            return data
          
          # If Morkato API Error
          raise geterr(data.get('extends', 'generic.unknown'), message=data.get('message'))

      except OSError as e:
        if tries < 4 and e.errno in (54, 10054):
          await asyncio.sleep(1 + tries * 2)
          continue
        raise

    raise error

  async def close(self) -> None:
    if self.__session:
      await self.__session.close()
  
  async def login(self, token: str) -> None:
    if self.loop == None:
      self.loop = asyncio.get_running_loop()

    if self.connector is None:
      self.connector = aiohttp.TCPConnector(limit=0)

    self.__session = aiohttp.ClientSession(
      connector=self.connector
    )
    
    self._global_over = asyncio.Event()
    self._global_over.set()

    old_token = self.token
    self.token = token