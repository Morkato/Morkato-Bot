from typing import Protocol, runtime_checkable

__all__ = (
  'GuildObject',
  'Snowflake',
  'WORKER',
  'EPOCH',
  'BITS',
  'SEQUENCE'
)

@runtime_checkable
class Snowflake(Protocol):
  id: int

@runtime_checkable
class GuildObject(Snowflake, Protocol):
  guild_id: int

WORKER = 1
EPOCH = 1672531200000
BITS  = 8
SEQUENCE = 24