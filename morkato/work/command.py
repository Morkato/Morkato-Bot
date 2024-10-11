from __future__ import annotations
from discord.ext.commands import Command
from typing import (
  TYPE_CHECKING,
  Optional,
  Any
)

if TYPE_CHECKING:
  from .extension import Extension

class MorkatoCommand(Command[Any, ..., Any]):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.extension: Optional[Extension] = None
  @property
  def cog(self) -> None:
    return None