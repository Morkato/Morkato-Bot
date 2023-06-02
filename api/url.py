from __future__ import annotations

from utils.types.generic import Headers, Json

from requests import Response, Session
from typing import Optional, Iterator, TypeVar, Union, overload, Any
from utils.string import format as format_str
from urllib.parse import quote

T = TypeVar('T')

class UrlSearchParams:
  def __init__(self, params: dict[str, str]) -> None:
    self.__params = params
  def __repr__(self) -> str:
    return '?%s'%'&'.join(f'{quote(key)}={quote(value)}' for key, value in self.__params.items()) if self.__params else ''
  def __getitem__(self, key: str, /) -> str:
    return self.__params[key]
  def __setitem__(self, key: str, value) -> None:
    if isinstance(value, str):
      self.__params[key] = value

      return
    self.__params[key] = str(value)
  def __iter__(self) -> Iterator[tuple[str, str]]:
    return iter(self.__params.items())
  def __len__(self) -> int:
    return len(self.__params)

  @overload
  def get(self, key: str) -> Union[str, None]: ...
  @overload
  def get(self, key: str, default: T) -> Union[str, T]: ...
  def get(self, key: str, default: Optional[T] = None) -> Union[str, T]:
    return self.__params.get(key, default)

  def set(self, key: str, value: str) -> None:
    self.__setitem__(key, value)

class Route:
  def __init__(self, route: str, uri: Union[Route, str], params: Optional[dict[str, str]] = None) -> None:
    if isinstance(uri, Route):
      params = {**uri.__params, **(params or {})}

      route = (uri.route.strip('/') + f"/{route.strip('/')}")
      uri = uri.url
    
    self.__uri = uri
    self.__route = [''] + route.strip('/').split('/')

    self.__params = params or {}
  
  def __repr__(self) -> str:
    return f"{self.__uri}{quote(self.route)}{self.params}"
  def __str__(self) -> str:
    return self.__repr__()

  @property
  def url(self) -> str:
    return self.__uri
  @property
  def route(self) -> str:
    return '/'.join(self.__route)
  @property
  def params(self) -> UrlSearchParams:
    return UrlSearchParams(self.__params)
  
  def setParam(self, key: str, value: str) -> None:
    self.__params[key] = value
  
  def getParam(self, key: str, /) -> Union[str, None]:
    return self.__params.get(key)
  
  def format(self, /, **kwargs) -> Route:
    url = format_str(self.url, **kwargs)
    path = format_str(self.route, **kwargs)

    return Route(path, url, self.__params)

class SessionRoute(Session):
  def __init__(self, route: Route, /, defaultHeaders: Optional[Headers] = None) -> None:
    super().__init__()

    self.__route = route
    self.__defaultHeaders = defaultHeaders or {}
  @overload
  def request(
    self, method: str | bytes,
    route: str | bytes,
    data = None,
    headers: Headers = None,
    cookies = None,
    files = None,
    auth = None,
    stream: bool | None = False,    
    json: Json | None = None
  ) -> Response: ...
  def request(self, method: str | bytes, route: str | bytes, *args, **kwargs) -> Response:
    return super().request(method, str(Route(route, self.__route)), *args, **kwargs, headers=kwargs.get('headers', self.__defaultHeaders))

def session(route: Route, /, defaultHeders: Optional[dict[str, Any]] = None) -> SessionRoute:
  return SessionRoute(route, defaultHeders)