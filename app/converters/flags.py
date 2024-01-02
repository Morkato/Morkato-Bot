from __future__ import annotations

from typing import (
  Optional,
  Tuple,
  TypeVar,
  Union,
  
  overload,

  TYPE_CHECKING,
  Dict,
  List
)

if TYPE_CHECKING:
  from discord.ext.commands.context import Context
  from morkato.bot import MorkatoBot

from discord.ext.commands.parameters import parameter
from discord.ext.commands.converter import Converter

import re

FlagDataType = Tuple[Union[str, None], dict[str, List[str]]]

T = TypeVar('T')
K = TypeVar('K')

class _FlagConverter(Converter):
  @classmethod
  async def convert(cls, ctx: Context[MorkatoBot], argument: str) -> FlagDataType:
    return parse(argument)

FlagConverter = parameter(converter=_FlagConverter, default=(None, {}))

base_pattern = r'^\s*(-[a-z]|--[a-z]+)?([^-].*)?$'

def sum_dict(dir1: dict[K, T], dir2: dict[K, T]) -> dict[K, T]:
  for key, value in dir1.items():
    if not key in dir2:
        continue
    
    dir1[key] = value + dir2.pop(key)

  return dir1 | dir2

def _parse(text: str) -> FlagDataType:
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

def parse(text: str) -> FlagDataType:
  return _parse(text)