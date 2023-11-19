__all___ = (
  'HTTPClient',
  'request',
)

from typing import (
  Optional,
  Generator,
  Callable,
  Coroutine,
  TypeVar,
  
  Any
)

from .request  import Request
from .response import Response
from .headers  import Headers

import aiohttp
import asyncio

import sys

http_version = '1.0'

T = TypeVar('T')

class RequestContext:
  __slots__ = ('_coro', '_resp')

  def __init__(self, coro: Coroutine[Any, Any, Response]) -> None:
    self._coro = coro
  
  def send(self, arg: None) -> asyncio.Future[Any]:
    return self._coro.send(arg)
  
  def throw(self, exp: Exception) -> None:
    self._coro.throw(exp)

  def close(self) -> None:
    return self._coro.close()
  
  def __await__(self) -> Generator[Any, None, Response]:
    return self._coro.__await__()
  
  def __iter__(self) -> Generator[Any, None, Response]:
    return self.__await__()
  
  async def __aenter__(self) -> Response:
    self._resp = await self
  
    return self._resp

  async def __aexit__(self, *args, **kwargs) -> None:
    await self._resp.end()

class HTTPClient:
  def __init__(
    self,
    loop: asyncio.AbstractEventLoop, *,
    headers: Optional[Headers] = None
  ) -> None:
    self._session: aiohttp.ClientSession = aiohttp.ClientSession(loop=loop)
    self.loop = loop

    user_agent = 'V1NI1313 (https://github.com/V1NI1313/Morkato-Bot {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
    self.user_agent: str = user_agent.format(http_version, sys.version_info, aiohttp.__version__)

    self.__headers = Headers(headers)

    self.__headers.set('user-agent', self.user_agent)

  async def __aenter__(self) -> "HTTPClient":
    return self

  async def __aexit__(self, *args, **kwargs) -> None:
    await self.close()

  @property
  def headers(self) -> Headers:
    return self.__headers
  
  async def ws(self, url: str) -> aiohttp.ClientWebSocketResponse:
    return await self._session.ws_connect(url)
  
  def request(self, request: Request, **kwargs) -> RequestContext:
    return RequestContext(self._request(request, **kwargs))
  
  async def _request(self, request: Request, **kwargs):
    req = self.make_request(request)

    method = req.method
    url    = str(req.url)

    kwargs = {
      'headers': req.headers.toJSON()
    }

    if req.body:
      kwargs['data'] = req.body

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