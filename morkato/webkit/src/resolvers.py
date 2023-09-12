from typing import (
  Callable,
  Coroutine,
  
  Any
)

from .response import Response

def json(decode: str) -> Callable[[Response], Coroutine[Any, Any, Any]]:
  async def resolver(res: Response) -> Coroutine[Any, Any, Any]:
    return await res.json()
  
  return resolver