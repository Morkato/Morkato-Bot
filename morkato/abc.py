from typing import Protocol, runtime_checkable

@runtime_checkable
class Snowflake(Protocol):
  id: int