from typing import Optional, Literal, Union, Dict, Any

from .errors import (
  HTTPException,
  BadRequest,
  Unauthorized,
  Forbidden,
  NotFound,
  MethodNotAllowed,
  TooManyRequests,
  InternalServerError
)

from urllib.parse import quote
from utils.etc import getEnv

import aiohttp
import asyncio
import json
import yarl
import ssl

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
    loop: asyncio.AbstractEventLoop
  ) -> None:
    self._session: aiohttp.ClientSession = aiohttp.ClientSession(loop=loop)
    self.loop = loop

    user_agent = 'V1NI1313 (https://github.com/V1NI1313/Morkato-Bot {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
    self.user_agent: str = user_agent.format(__version__, sys.version_info, aiohttp.__version__)
  async def __aenter__(self) -> "HTTPClient":
    return self
  async def __aexit__(self, *args, **kwargs) -> None:
    await self.close()

  async def ws(self, url: str, compress: int = 0) -> aiohttp.ClientWebSocketResponse:
    kwargs = {
      'headers': {
          'User-Agent': self.user_agent,
      },
      'compress': compress
    }

    return await self._session.ws_connect(url, **kwargs)
  async def request(self, route: Route, **kwargs):
    method = route.method
    url = route.url

    headers = {
      'User-Agent': self.user_agent
    }

    if kwargs.get('json'):
      headers['Content-Type'] = 'application/json'
      kwargs['data'] = json.dumps(kwargs.pop('json'))
    
    if kwargs.get('auth'):
      headers['Authorization'] = kwargs.pop('auth')
    
    kwargs['headers'] = headers

    res: aiohttp.ClientResponse = None
    data: Union[Dict[str, Any], str] = None

    for tries in range(5):
      try:
        async with self._session.request(method, url, **kwargs) as res:
          data = await json_or_text(res)

          if res.status in {500, 502, 504, 524}:
            await asyncio.sleep(1 + tries * 2)
            continue
        
        if not res.status == 200:
          if res.status == 400:
            raise BadRequest(res, data)
          elif res.status == 401:
            raise Unauthorized(res, data)
          elif res.status == 403:
            raise Forbidden(res, data)
          elif res.status == 404:
            raise NotFound(res, data)
          elif res.status == 405:
            raise MethodNotAllowed(res, data)
          elif res.status == 429:
            raise TooManyRequests(res, data)
          elif res.status >= 500:
            raise InternalServerError(res, data)
          
          raise HTTPException(res, data)
        
        return data
      except OSError as e:
        if tries < 4 and e.errno in (54, 10054):
          await asyncio.sleep(1 + tries * 2)
          continue
        raise

    if not res is None:
      raise HTTPException(res, data)
    
    raise RuntimeError('Unreachable code in HTTP handling')
  
  async def close(self) -> None:
    await self._session.close()