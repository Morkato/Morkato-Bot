from __future__ import annotations
from typing import (
  TYPE_CHECKING,
  runtime_checkable,
  Iterator,
  Optional,
  Protocol,
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

@runtime_checkable
class ToRegistryObject(Protocol):
  __registry_class__: bool
@runtime_checkable
class SelectMenuObject(Protocol):
  name: str
  id: int
  banner: Optional[str]
@runtime_checkable
class ArrayType(Protocol[T]):
  def __getitem__(self, key: int, /) -> T: ...
  def __iter__(self) -> Iterator[T]: ...
  def __len__(self) -> int: ...