from aiohttp import ClientResponse

from .headers import Headers

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

import json

class Response:
  def __init__(self, res: ClientResponse) -> None:
    self.__response = res

    self.__headers = Headers(res.headers)

  async def __aenter__(self) -> "Response":
    return self
  
  async def __aexit__(self, *args, **kwargs) -> None:
    await self.end()

  @property
  def closed(self):
    return self.__response.closed
  
  @property
  def headers(self) -> Headers:
    return self.__headers
  
  @property
  def status_code(self) -> int:
    return self.__response.status
  
  async def raise_for_status(self) -> None:
    res = self.__response
    
    if not self.status_code >= 200 and not self.status_code < 300:

      data = await self.content()

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
  async def content(self, bytes: int = -1) -> str:
    if bytes == -1:
      return await self.__response.text()
    
    return next((item async for item in self.content_was(bytes)), '')

  async def json(self) -> dict:
    return json.loads(await self.content())

  async def content_was(self, bytes: int = 4096):
    async for chunk in self.__response.content.iter_chunked(bytes):
      yield chunk

  async def end(self) -> None:
    if not self.closed:
      await self.__response.close()