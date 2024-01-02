from __future__ import annotations

from typing_extensions import Self
from typing import (
  Optional,
  Coroutine,
  Callable,
  Union,
  
  TYPE_CHECKING,
  List,
  Dict,
  Any
)

if TYPE_CHECKING:
  from morkato.context import MorkatoContext

  EmptyCoro = Coroutine[Any, Any, None]

import asyncio
import inspect

BaseType = Union[str, None]
FlagDataType = List[str]
FlagType = Dict[str, FlagDataType]

FlagCallback = Union[
  Callable[[Self, 'MorkatoContext'], 'EmptyCoro'],
  Callable[[Self, 'MorkatoContext', BaseType], 'EmptyCoro'],
  Callable[[Self, 'MorkatoContext', BaseType, FlagDataType], 'EmptyCoro'],
  Callable[[Self, 'MorkatoContext', BaseType, FlagDataType, FlagType], 'EmptyCoro']
]

def create_callback(call: FlagCallback):
  signatured = inspect.signature( call)

  parameters = signatured.parameters

  length = len(parameters) - 1

  if length < 1:
    raise Exception(f'Internal error in event `{call.__name__}`')
  
  async def wrapper(self, ctx: MorkatoContext, base: BaseType, flag: List[str], flags: Dict[str, List[str]]) -> None:
    required_params = [self, ctx]
    optional_params = [base, flag, flags]

    parameters = required_params + optional_params[:length - 1]

    return await call(*parameters)
  
  return wrapper

class Flag:
  def __init__(self, call: FlagCallback, *, name: str, aliases: Optional[List[str]] = None) -> None:
    if not asyncio.iscoroutinefunction(call):
      raise TypeError
    
    self.group: GroupFlagMeta = None # type: ignore
    
    self.name     = name
    self.callback = create_callback(call)
    self.aliases  = aliases or []

  async def invoke(self, ctx: MorkatoContext, base: Union[str, None], flag: List[str], flags: Dict[str, List[str]]) -> None:
    try:    
      return await self.callback(self.group, ctx, base, flag, flags)
    except Exception as err:
      raise

class GroupFlagMeta(type):
  __flags__: List[Flag] = []

  def __new__(cls, name: str, bases: Any, attrs: Dict[str, Any], **kwargs) -> Self:
    flags = []
    
    for base in bases:
      if not issubclass(base, FlagGroup):
        continue

      flags += base.__flags__

    for key, item in attrs.items():
      if not isinstance(item, Flag) or key.startswith('__'):
        continue

      flags.append(item)

    attrs['__flags__'] = flags

    return super().__new__(cls, name, bases, attrs, **kwargs)

class FlagGroup(metaclass=GroupFlagMeta):
  def __init__(self) -> None:
    for flag in self.__class__.__flags__:
      flag.group = self
  
  async def invoke(self, ctx: MorkatoContext, base: BaseType, flags: FlagType) -> bool:
    cls = self.__class__
  
    if not flags:
      return False
    
    iterable = iter(flags.items())
    
    key, value = next(iterable)

    flagger = next((flag for flag in cls.__flags__ if flag.name == key or key in flag.aliases), None)

    if not flagger:
      return False

    flags.pop(key, None)

    await flagger.invoke(ctx, base, value, flags)

    return True

def flag(*, name: Optional[str] = None, aliases: Optional[List[str]] = None) -> Callable[[FlagCallback], Flag]:
  def wrapper(func: FlagCallback) -> Flag:
    return Flag(
      func,
      name=name or func.__name__,
      aliases=aliases
    )
  
  return wrapper