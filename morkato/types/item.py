from typing import TypedDict, Optional

__all__ = (
  'Item',
)

class Item(TypedDict):
  name: str
  description: Optional[str]

  guild_id: str
  id:       str

  usable: bool
  stack: int
  
  embed_title:       Optional[str]
  embed_description: Optional[str]
  embed_url:         Optional[str]

  updated_at: int
