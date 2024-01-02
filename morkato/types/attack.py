from typing import TypedDict, Union

__all__ = (
  'Attack',
)

class Attack(TypedDict):
  name: str
  id: str

  required_exp: int

  damage: int
  breath: int
  blood:  int

  guild_id:  str

  embed_title:       Union[str, None]
  embed_description: Union[str, None]
  embed_url:         Union[str, None]
  
  art_id:    Union[str, None]
  item_id:   Union[str, None]
  parent_id: Union[str, None]

  updated_at: Union[int, None]