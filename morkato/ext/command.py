from __future__ import annotations
from discord.ext.commands import Command
from typing import (
  TYPE_CHECKING,
  Optional,
  Type
)

if TYPE_CHECKING:
  from .extension import Extension

class MorkatoCommand(Command):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self._extension: Optional[Extension] = None
  @property
  def cog(self) -> None:
    return None