from typing import Optional, TypeVar, Union, overload

from decouple import config

T = TypeVar('T')

@overload
def getEnv(key: str) -> Union[str, None]: ...
@overload
def getEnv(key: str, default: T) -> Union[str, T]: ...
def getEnv(key: str, default: Optional[T] = None) -> Union[str, None, T]:
  try:
    return str(config(key))
  except:
    return default