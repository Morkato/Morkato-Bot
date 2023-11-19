from __future__ import annotations

from typing import (
  Optional,
  TypeVar,
  Union,
  
  overload,

  TYPE_CHECKING,
  Dict,
  List
)

from discord.ext import commands

if TYPE_CHECKING:
  from ..context import MorkatoContext

import re

T = TypeVar('T')
K = TypeVar('K')

base_pattern = r'^\s*(-[a-z]|--[a-z]+)?([^-].*)?$'

def sum_dict(dir1: dict[K, T], dir2: dict[K, T]) -> dict[K, T]:
  for key, value in dir1.items():
    if not key in dir2:
        continue
    
    dir1[key] = value + dir2.pop(key)

  return dir1 | dir2

def _parse(text: str) -> tuple[Union[str, None], dict[str, str]]:
  result = None

  try:
    result = list(re.match(base_pattern, text, re.IGNORECASE).groups())
  except:
    return (None, {})

  params = {}

  if not result[0]:
    if not result[1]:
      return (None, params)

    flag = re.search(r'\s(-[a-z]|--[a-z]+)', result[1], re.IGNORECASE)

    if not flag:
      return (result[1], params)

    start, _ = flag.span()
    
    text = result[1][start+1:]

    _, params = _parse(text)

    return (result[1][:start].strip() or None, params)
    
  result[0] = re.sub(r'^--?', '', result[0])

  if not result[1]:
    params[result[0]] = []

    return (None, params)
  
  param_value, other_params = _parse(result[1])

  params[result[0]] = [param_value] if param_value else []
  
  return (None, sum_dict(params, other_params))

def parse(text: str) -> tuple[Union[str, None], dict[str, str]]:
  return _parse(text)

class Context:
  def __init__(self, base: Union[str, None] = None, params: Optional[Dict[str, List[str]]] = None) -> None:
    self.__base = base
    self.__params = params or {}
  
  def __repr__(self) -> str:
    return self.__base + repr(self.__params)
  
  @property
  def base(self) -> Union[str, None]:
    return self.__base
  
  @property
  def params(self) -> Dict[str, List[str]]:
    return self.__params
  
  @overload
  def get(self, k: str) -> Union[List[str], None]: ...
  @overload
  def get(self, k: str, d: T) -> Union[List[str], T]: ...
  def get(self, k: str, d: Optional[T] = None) -> Union[List[str], T, None]:
    return self.__params.get(k, d)
  
class CommandConverter(commands.Converter, Context):
  async def convert(self, ctx: MorkatoContext, argument: str) -> Context:
    result = parse(argument)

    return Context(*result)