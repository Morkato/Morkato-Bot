from __future__ import annotations

from typing import (
  Optional,
  Union,
  
  TYPE_CHECKING,
  Dict,
  List,
  Any
)

from .types.command import CommandFunction

from discord.ext     import commands
from objects.guild   import Guild

import inspect

if TYPE_CHECKING:
  from .command import Command

def make_event(
  event: CommandFunction
):
  async def wrapper(
    ctx:      commands.Context,
    this:     Command,
    guild:    Guild,
    util:     Any,
    value:    Optional[Union[str, None]] = None,
    value_in: Optional[Union[str, None]] = None,
    params:   Optional[Dict[str, str]]   = None
  ) -> None:
    signatured = inspect.signature(event)

    parameters = signatured.parameters

    length = len(parameters) - 1

    if length < 2:
      raise Exception(f'Internal error in event `{event.__name__}`')
    
    required_params = [ctx, guild]
    optional_params = [util, value, value_in, params]

    length_params = length - 2
    
    event_params = required_params + optional_params[:length_params]

    print(event_params)

    print(inspect.signature(event))
    
    return await event(this, *event_params)

  return wrapper

class Flag:
  def __init__(self, *, name: str, aliases: Optional[List[str]] = None, func: CommandFunction) -> None:
    self.event = make_event(func)

    self.__name = name

    self.__aliases: List[str] = [name,] + (aliases or [])

  async def __call__(
    self,
    this:     Command,
    ctx:      commands.Context,
    guild:    Guild,
    util:     Any,
    value:    Optional[Union[str, None]] = None,
    value_in: Optional[Union[str, None]] = None,
    params:   Optional[Dict[str, str]]   = None
  ) -> None:
    return await self.event(
      ctx,
      this,
      guild,
      util,
      value,
      value_in,
      params
    )
  
  @property
  def name(self) -> str:
    return self.__name
  
  @property
  def aliases(self) -> List[str]:
    return self.__aliases

def flag(*, name: str, aliases: Optional[List[str]] = None):
  def wrapper(func: CommandFunction) -> Flag:
    return Flag(
      name=name,
      aliases=aliases,
      func=func
    )
  
  return wrapper
