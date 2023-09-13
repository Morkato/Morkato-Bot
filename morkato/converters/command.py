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

from discord.ext         import commands
from parsers.command_bar import parse

if TYPE_CHECKING:
  from ..context import MorkatoContext

T = TypeVar('T')

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

    print(result)

    return Context(*result)