from typing import (
  Literal,
  TypedDict,
  Union
)

__all__ = (
  'PlayerBreedType',
  'Player'
)

PlayerBreedType = Literal['HUMAN', 'ONI', 'HYBRID']

class Player(TypedDict):
  name:        str
  credibility: int
  history:     Union[str, None]
  
  guild_id: str
  id:       str
  breed:    PlayerBreedType

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

  updated_at: Union[int, None]