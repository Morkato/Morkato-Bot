from typing import (
  Literal,
  TypedDict,
  Union
)

PlayerBreed = Literal['HUMAN', 'ONI', 'HYBRID']

class Player(TypedDict):
  name:        str
  credibility: int
  
  guild_id: str
  id:       str
  breed:    PlayerBreed

  cash: int

  life:   int
  blood:  int
  breath: int
  exp:    int

  appearance:   Union[str, None]
  webhook_link: str

