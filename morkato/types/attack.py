from typing import TypedDict, Union

__all__ = (
  'Attack',
)

class Attack(TypedDict):
  name: str

  required_exp: int

  damage: int
  breath: int
  blood:  int

  guild_id:  str
  art_id:    Union[str, None]
  item_id:   Union[str, None]
  parent_id: Union[str, None]

  created_at: str
  updated_at: str