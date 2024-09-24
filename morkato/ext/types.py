from __future__ import annotations
from typing import (
  TYPE_CHECKING,
  Concatenate,
  Callable,
  Coroutine,
  TypeVar,
  Any
)
if TYPE_CHECKING:
  from .extension import Extension
  ListenerFuncType = Callable[Concatenate[Extension, ...], "Coro[None]"]
else:
  ListenerFuncType = Any
T = TypeVar('T')
CoroAny = Coroutine[Any, Any, Any]
Coro = Coroutine[Any, Any, T]
