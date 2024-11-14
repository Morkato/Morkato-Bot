from typing import (
  runtime_checkable,
  Protocol,
  TypeVar
)

@runtime_checkable
class ObjectWithPercent(Protocol):
  id: int
  percent: int
@runtime_checkable
class RolledObjectModel(Protocol):
  name: str
  id: int
  percent: int
ObjectWithPercentT = TypeVar('ObjectWithPercentT', bound=ObjectWithPercent)