from typing import Optional, TypedDict, Literal, Union, List

class AttackField(TypedDict):
  id: str

  text: str
  roles: List[str]

class Attack(TypedDict):
  name: str

  roles: List[str]
  required_roles: int

  damage: int
  stamina: int

  embed_title: Union[str, None]
  embed_description: Union[str, None]
  embed_url: Union[str, None]

  fields: List[AttackField]

class Art(TypedDict):
  name: str
  type: Literal['RESPIRATION', 'KEKKIJUTSU', 'ATTACK']
  role: Union[str, None]

  embed_title: Union[str, None]
  embed_description: Union[str, None]
  embed_url: Union[str, None]

  attacks: List[Attack]

class Respiration(Art):
  type: Literal["RESPIRATION"]

class Kekkijutsu(Art):
  type: Literal["KEKKIJUTSU"]