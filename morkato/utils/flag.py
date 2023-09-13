from __future__ import annotations

from typing_extensions import Self
from typing import (
  Callable,
  Union,
  
  TYPE_CHECKING,
  List,
  Dict,
  Any
)

if TYPE_CHECKING:
  from morkato.context import MorkatoContext

from .etc import EmptyCoro, UNDEFINED, case_undefined

import asyncio
import inspect

FlagCallback = Union[Callable[[Self, 'MorkatoContext'], 'EmptyCoro'], Callable[[Self, 'MorkatoContext', Union[str, None]], 'EmptyCoro'], Callable[[Self, 'MorkatoContext', Union[str, None], List[str]], 'EmptyCoro']]

def make_callback(call: FlagCallback):
  signatured = inspect.signature( call)

  parameters = signatured.parameters

  length = len(parameters) - 1

  if length < 1:
    raise Exception(f'Internal error in event `{call.__name__}`')
  
  async def wrapper(self, ctx: MorkatoContext, base: Union[str, None], param: List[str]) -> None:
    required_params = [self, ctx]
    optional_params = [base, param]

    params = required_params + optional_params[:length - 1]

    return await call(*params)
  
  return wrapper

class Flag:
  def __init__(self, call: FlagCallback, *, name: str, aliases: List[str] = UNDEFINED) -> None:
    if not asyncio.iscoroutinefunction(call):
      raise TypeError
    
    self.group: GroupFlagMeta = None # type: ignore
    
    self.name     = name
    self.callback = make_callback(call)
    self.aliases  = case_undefined(aliases, [])

  async def __call__(self, ctx: MorkatoContext, base: Union[str, None], param: List[str]) -> None:
    return await self.callback(self.group, ctx, base, param)

class GroupFlagMeta(type):
  __flags__: List[Flag] = []

  def __new__(cls, name: str, bases: Any, attrs: Dict[str, Any], **kwargs) -> Self:
    flags = []

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

def flag(*, name: str = UNDEFINED, aliases: List[str] = UNDEFINED):
  def wrapper(func: FlagCallback) -> Flag:
    return Flag(
      func,
      name=case_undefined(name, func.__name__),
      aliases=aliases
    )
  
  return wrapper

async def process_flags(group: FlagGroup, *, ctx: MorkatoContext, base: Union[str, None], params: Dict[str, List[str]]) -> None:
  if not params:
    return
  
  key, value = next(iter(params.items()))

  event = next((flag for flag in group.__class__.__flags__ if flag.name == key or key in flag.aliases), None)

  if not event:
    await ctx.send('Essa flag não existe :/')

    return
  
  await event(ctx, base, value)