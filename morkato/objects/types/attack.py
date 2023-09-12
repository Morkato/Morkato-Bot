from typing import TypedDict

class Attack(TypedDict):
  name: str

  required_exp:   int

  damage:  int
  stamina: int

  guild_id:  str
  art_id:    str
  parent_id: str

  created_at: str
  updated_at: str