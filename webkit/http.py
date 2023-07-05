from typing import Optional, Callable, Literal, Union, Coroutine, TypeVar, Dict, Any

from .headers  import Headers, _Headers
from .request  import Request
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

    self.__headers = Headers(headers)

    self.__headers.set('user-agent', self.user_agent)

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
  async def request(self, request: Request, **kwargs):
    req = self.make_request(request)

    method = req.method
    url    = str(req.url)

    if kwargs.get('json'):
      kwargs['data'] = json.dumps(kwargs.pop('json'))

      req.headers.set('content-type', 'application/josn')

    kwargs = {
      'headers': req.headers.toJSON()
    }
      

    for tries in range(5):
      try:
        return Response(await self._session.request(method, url, **kwargs))
      except OSError as e:
        if tries < 4 and e.errno in (54, 10054):
          await asyncio.sleep(1 + tries * 2)
          continue
        raise
    
    raise RuntimeError('Unreachable code in HTTP handling')
  
  def make_request(self, req: Request) -> Request:
    req.headers.extend(self.__headers)

    return req
  
  async def close(self) -> None:
    await self._session.close()

async def request(request: Request, *, call: Callable[[Response], Coroutine[Any, Any, T]]) -> T:
  loop = asyncio.get_event_loop()

  async with HTTPClient(loop) as client:
    res = await client.request(request)
    data = await call(res)

    await res.end()

    return data

    

