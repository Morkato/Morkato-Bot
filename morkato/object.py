from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  SupportsInt,
  Optional,
  Type,
  Any
)

if TYPE_CHECKING:
  from .abc import Snowflake

from .utils.etc import (
  MORKATO_SNOWFLAKE_BITS,
  MORKATO_SNOWFLAKE_SEQ
)

__all__ = (  
  'Object',
)

class Object:
  def __init__(self, id: SupportsInt, *, type: Optional[Type[Snowflake]] = None) -> None:
    try:
      id = int(id)
    except ValueError:
      raise TypeError

    self.id: int = id
    self.type: Type[Snowflake] = type or self.__class__
  
  def __repr__(self) -> str:
    return f'<Object id={self.id!r} type={self.type!r}>'
  
  def __eq__(self, other: Any) -> bool:
    return isinstance(other, self.type) and self.id == other.id
  
  def __hash__(self) -> int:
    return self.id >> (MORKATO_SNOWFLAKE_BITS + MORKATO_SNOWFLAKE_SEQ)