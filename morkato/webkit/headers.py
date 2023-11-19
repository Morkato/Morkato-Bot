from __future__ import annotations

__all__ = (
  'Headers',
)

from typing import (
  Optional,
  Literal,
  TypeVar,
  Union,
  
  Dict,
  
  overload
)

from copy import deepcopy

_HeadersKeys = Literal[
  "user-agent",
  "accept",
  "accept-language",
  "authorization",
  "accept-encoding",
  "referer",
  "connection",
  "upgrade-insecure-requests",
  "if-modified-since",
  "if-none-match",
  "cache-control",

  "content-type",
  "content-length"
]

_Headers = Dict[_HeadersKeys, Optional[str]]

T = TypeVar('T')

class Headers:
  def __init__(self, init: Union[_Headers, "Headers", None] = None) -> None:
    if isinstance(init, Headers):
      self.from_copy(init)
    
      return
    
    self._load_variables(init)

  def __repr__(self) -> str:
    return repr(self.__headers)
  
  def __getitem__(self, key: _HeadersKeys) -> Union[str, None]:
    return self.get(key)
  
  def __setitem__(self, k: _HeadersKeys, vt: str) -> None:
    self.set(k, vt)
  
  def __add__(self, other: Union[_Headers, Headers]) -> Headers:
    return deepcopy(self).extend(other)

  def _load_variables(self, payload: Optional[_Headers] = None) -> None:
    self.__headers = payload or {}
    
  @property
  def all(self) -> _Headers:
    return self.__headers
  
  def from_copy(self, headers: "Headers") -> None:
    self._load_variables(headers.all)

  @overload
  def get(self, k: _HeadersKeys) -> Union[str, None]: ...
  @overload
  def get(self, k: _HeadersKeys, dt: T) -> Union[str, T]: ...
  def get(self, k: _HeadersKeys, dt: Optional[T] = None) -> Union[str, T]:
    return next((item for key, item in self.__headers.items() if key.lower() == k.lower()), dt)

  def set(self, k: _HeadersKeys, vt: str, *, copy: bool = False) -> "Headers":
    if copy:
      return deepcopy(self).set(k, vt)
    
    self.__headers[k] = vt

    return self
  
  def extend(self, other: Union[_Headers, "Headers"]) -> "Headers":
    if isinstance(other, Headers):
      other = other.all

    self.__headers |= other

    return self
  
  def toJSON(self) -> _Headers:
    return self.all