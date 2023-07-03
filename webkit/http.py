from typing import Optional, Callable, Literal, Union, Coroutine, TypeVar, Dict, Any

from .headers import Headers, _Headers
from .response import Response

from urllib.parse import quote
from utils.etc import getEnv

import aiohttp
import asyncio
import json
import yarl

import sys

__version__ = '1.0'

Methods = Literal[
  'GET',
  'PUT',
  'POST',
  'PATCH',
  'DELETE',
  'OPTIONS'
]

async def json_or_text(res: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
  text = await res.text()

  try:
    if res.headers['content-type'] == 'application/json':
      return json.loads(text)
  except:
    pass

  return text

T = TypeVar('T')

class Route:
  URL        = yarl.URL(getEnv('URL', 'http://localhost:80'))
  WEB_SOCKET = getEnv('GATEWAY', 'wss://localhost:80')

  def __init__(self, method: Methods, path: str, *, metadata: Optional[str] = None, **parameters) -> None:
    self.path: str = path
    self.method: str = method
    self.metadata: Optional[str] = metadata
    
    url = str(self.URL) + self.path
    
    if parameters:
      url = url.format_map({k: quote(v) if isinstance(v, str) else v for k, v in parameters.items()})
    
    self.url: str = url

  @property
  def key(self) -> str:
    if self.metadata:
      return f'{self.method} {self.path}:{self.metadata}'
    return f'{self.method} {self.path}'

class HTTPClient:
  URL = Route.URL
  
  def __init__(
    self,
    loop: asyncio.AbstractEventLoop, *,
    headers: Optional[Headers] = None
  ) -> None:
    self._session: aiohttp.ClientSession = aiohttp.ClientSession(loop=loop)
    self.loop = loop

    user_agent = 'V1NI1313 (https://github.com/V1NI1313/Morkato-Bot {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
    self.user_agent: str = user_agent.format(__version__, sys.version_info, aiohttp.__version__)

    self.__headers = headers or Headers()
  async def __aenter__(self) -> "HTTPClient":
    return self
  async def __aexit__(self, *args, **kwargs) -> None:
    await self.close()

  @property
  def headers(self) -> Headers:
    return self.__headers
  
  async def ws(self, url: str, compress: int = 0) -> aiohttp.ClientWebSocketResponse:
    kwargs = {
      'headers': {
          'User-Agent': self.user_agent,
      },
      'compress': compress
    }

    return await self._session.ws_connect(url, **kwargs)
  async def request(self, route: Route, headers: Union[Headers, _Headers, None] = None, **kwargs):
    method = route.method
    url = route.url

    headers = headers if isinstance(headers, Headers) else Headers(headers)

    headers.set('user-agent', self.user_agent)

    if kwargs.get('json'):
      headers.set('content-type', 'application/json')
      
      kwargs['data'] = json.dumps(kwargs.pop('json'))
    
    if kwargs.get('auth'):
      headers.set('authorization', kwargs.pop('auth'))
    
    kwargs['headers'] = headers.extend(self.headers).toJSON()

    for tries in range(5):
      try:
        return Response(await self._session.request(method, url, **kwargs))
      except OSError as e:
        if tries < 4 and e.errno in (54, 10054):
          await asyncio.sleep(1 + tries * 2)
          continue
        raise
    
    raise RuntimeError('Unreachable code in HTTP handling')
  
  async def close(self) -> None:
    await self._session.close()

async def request(route: Route, headers: Union[Headers, _Headers, None] = None, *, call: Callable[[Response], Coroutine[Any, Any, T]], **kwargs):
  loop = asyncio.get_event_loop()

  async with HTTPClient(loop) as client:
    res = await client.request(route, headers, **kwargs)
    data = await call(res)

    await res.end()

    return data

    

