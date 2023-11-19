__all__ = (
  'URLParameters',
  'URLRoute',
  'URL',
  'Request',
)

from typing import (
  Optional,
  Literal,
  TypeVar,
  Union,
  
  Any,
  
  overload
)

from urllib.parse import quote

from .headers import Headers

import json
import yarl
import re
import os

T = TypeVar('T')

Methods = Literal[
  'GET',
  'PUT',
  'POST',
  'PATCH',
  'DELETE',
  'OPTIONS'
]

def resolve_body(body: Any) -> tuple[str, Union[str, bytes]]:
  if isinstance(body, ( bytes, bytearray )):
    return (
      "application/octet-stream",
      body
    )
  
  elif isinstance(body, ( dict, list, str, int, float, bool )):
    return (
      "application/json",
      json.dumps(body)
    )
    
  raise Exception('Invalid body')

class URLParameters:
  def __init__(self, **params) -> None:
    self.__parameters = params

  def __bool__(self) -> bool:
    return bool(self.__parameters)
  
  def __repr__(self) -> str:
    if self.__parameters:
      return ('?' + '&'.join(f'{key}={quote(str(value))}' for key, value in self.__parameters.items()))
    
    return ''
  
  @overload
  def get(self, k: str) -> Union[str, None]: ...
  @overload
  def get(self, k: str, default: T) -> Union[str, T]: ...
  def get(self, k: str, default: Optional[T] = None) -> Union[str, T]:
    return self.__parameters.get(k, default)
  
  def set(self, k: str, v: Any) -> None:
    if not isinstance(v, str):
      v = str(v)

    self.__parameters[k] = v

class URLRoute:
  def __init__(self, route: Union["URLRoute", str, None] = None) -> None:
    if isinstance(route, str):
      index = route.find('?')

      route = route if index == -1 else route[:index-1]

    self.__route = str(route or '/')

    self.__route = re.sub(r'\/\/+', '/', self.__route)
    
  def __repr__(self) -> str:
    return '/' + self.__route.strip('/')
  
  def __add__(self, other: "URLRoute") -> "URLRoute":
    return URLRoute(str(self) + str(other))
  
  def __bool__(self) -> bool:
    return not self.__route == '/'

class URL:
  """
    Uma simples classe para interpretar URLs

    Parâmetros:
      route: Define a rota da URL (Requerido)

      url: Define a URL base para a aplicação (Opcional)
      parameters: Define os parâmetros da URL (Opcional)
    
    Exemplo:

      >>> url = URL('/hello word') # output: http://localhost/hello%02word
  """
  
  URL = os.getenv('URL', 'http://localhost:5500')

  def __init__(
    self,
    route:      Optional[Union[URLRoute, str, None]] = None, *,
    url:        Optional[Union[str, yarl.URL]]       = None,
    parameters: Optional[URLParameters]              = None
  ) -> None:
    self.__url = yarl.URL(url or self.URL)

    self.__route = URLRoute(route)

    self.__parameters = parameters or URLParameters()

  def __repr__(self) -> str:
    if self.__route:
      return f"{self.__url}{self.__route}{self.__parameters}"
    
    return f"{self.__url}{self.__parameters}"
  
  @property
  def url(self) -> yarl.URL:
    return self.__url
  
  @property
  def route(self) -> URLRoute:
    return self.__route
  
  @property
  def params(self) -> URLParameters:
    return self.__parameters

class Request:
  def __init__(self, method: Methods, url: Optional[Union[URL, str]] = None, *, headers: Optional[Headers] = None, body: Optional[Any] = None) -> None:
    self.__method = method
    self.__uri    = URL(url) if not url or isinstance(url, str) else url

    self.__headers = Headers(headers)

    self.__body = body

    if not body is None:
      (content_type, content) = resolve_body(body)

      self.__headers.set('content-type', content_type)

      self.__body = content

  def __repr__(self) -> str:
    return f'{self.__method} \"{self.__uri.route}\" from {self.__uri.url}'
  
  @property
  def method(self) -> str:
    return self.__method
  
  @property
  def url(self) -> URL:
    return self.__uri
  
  @property
  def headers(self) -> Headers:
    return self.__headers
  
  @property
  def body(self) -> Union[bytes, None]:
    return self.__body
  
  def setMethod(self, m: Methods) -> None:
    self.__method = m