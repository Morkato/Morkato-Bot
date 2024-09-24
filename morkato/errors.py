from aiohttp import ClientResponse
from typing import Optional

class MorkatoException(Exception):
  pass
class HTTPException(MorkatoException):
  def __init__(self, response: ClientResponse, message: Optional[str]):
    self.response: ClientResponse = response
    self.status: int = response.status
    self.text: str = message
class NotFoundError(HTTPException):
  pass
class MorkatoServerError(HTTPException):
  pass