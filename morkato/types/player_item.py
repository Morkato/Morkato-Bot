from typing import TypedDict, Optional

__all__ = (
  'PlayerItem',
)

class PlayerItem(TypedDict):
  guild_id: set
  player_id: str
  item_id: str

  stack: int
  
  created_at: int