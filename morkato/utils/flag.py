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
  from morkato.client  import Cog

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
  
  async def wrapper(self, ctx: MorkatoContext, base: Union[str, None], param: List[str], params: Dict[str, List[str]]) -> None:
    required_params = [self, ctx]
    optional_params = [base, param, params]

    parameters = required_params + optional_params[:length - 1]

    return await call(*parameters)
  
  return wrapper

class Flag:
  def __init__(self, call: FlagCallback, *, name: str, aliases: List[str] = UNDEFINED) -> None:
    if not asyncio.iscoroutinefunction(call):
      raise TypeError
    
    self.group: GroupFlagMeta = None # type: ignore
    
    self.name     = name
    self.callback = make_callback(call)
    self.aliases  = case_undefined(aliases, [])

  async def on_error(self, ctx: MorkatoContext, err: Exception) -> None:
    if hasattr(self, '_err'):
      return await self._err(self.group, ctx, err)
    
    raise err

  def error(self, func) -> Any:
    signatured = inspect.signature(func)

    parameters = signatured.parameters

    length = len(parameters) - 1

    if length < 1 or not asyncio.iscoroutinefunction(func):
      raise TypeError
    
    self._err = func

    return func

  async def __call__(self, ctx: MorkatoContext, base: Union[str, None], param: List[str], params: Dict[str, List[str]]) -> None:
    try:    
      return await self.callback(self.group, ctx, base, param, params)
    except Exception as err:
      await self.on_error(ctx, err)

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
  def __init__(self, cog: Cog) -> None:
    self.cog = cog
    self.bot = cog.bot
    
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
  
  iterable = iter(params.items())
  
  key, value = next(iterable)

  event = next((flag for flag in group.__class__.__flags__ if flag.name == key or key in flag.aliases), None)

  if not event:
    await ctx.send('Essa flag não existe :/')

    return

  params.pop(key, None)

  await event(ctx, base, value, params)