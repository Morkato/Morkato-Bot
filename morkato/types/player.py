from typing import (
  Literal,
  TypedDict,
  Union
)

__all__ = (
  'PlayerBreed',
  'Player'
)

PlayerBreed = Literal['HUMAN', 'ONI', 'HYBRID']

class PlayerItem(TypedDict):
  item_id: set
  stack: int

class Player(TypedDict):
  name:        str
  credibility: int
  history:     Union[str, None]
  
  guild_id: str
  id:       str
  breed:    PlayerBreed

  cash: int

  life:       int
  blood:      int
  breath:     int
  exp:        int
  force:      int
  resistance: int
  velocity:   int

  appearance: Union[str, None]
  banner:     Union[str, None]

  updated_at: int

