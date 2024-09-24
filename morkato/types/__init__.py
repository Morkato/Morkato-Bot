from __future__ import annotations
from typing import (
  TypedDict,
  Optional,
  Literal,
  List
)
RespirationType = Literal["RESPIRATION"]
KekkijutsuType = Literal["KEKKIJUTSU"]
FightingStyleType = Literal["FIGHTING_STYLE"]
ArtType = Literal[RespirationType, KekkijutsuType, FightingStyleType]
HumanType = Literal["HUMAN"]
OniType = Literal["ONI"]
HybridType = Literal["HYBRID"]
NpcType = Literal[HumanType, OniType, HybridType]
AlwaysActivateType = Literal["ALWAYS_ACTIVATE"]
RequiredActivateType = Literal["REQUIRED_ACTIVATE"]
AbilityType = Literal[AlwaysActivateType, RequiredActivateType]
class Art(TypedDict):
  name: str
  guild_id: str
  id: str
  type: ArtType
  description: Optional[str]
  banner: Optional[str]
  updated_at: Optional[int]
class ArtWithAttacks(TypedDict):
  attacks: List[Attack]
class Attack(TypedDict):
  name: str
  guild_id: str
  id: str
  art_id: str
  name_prefix_art: Optional[str]
  description: Optional[str]
  resume_description: Optional[str]
  banner: Optional[str]
  damage: int
  breath: int
  blood: int
  intents: int
  updated_at: Optional[int]
class Npc(TypedDict):
  guild_id: str
  id: str
  name: str
  surname: str
  type: NpcType
  family_id: Optional[str]
  energy: int
  max_life: int
  max_breath: int
  max_blood: int
  current_life: int
  current_breath: int
  current_blood: int
  icon: Optional[str]
class Ability(TypedDict):
  guild_id: str
  id: str
  name: str
  type: AbilityType
  percent: int
  npc_kind: int
  immutable: bool
  description: Optional[str]
  banner: Optional[str]
class Family(TypedDict):
  guild_id: str
  id: str
  name: str
  description: Optional[str]
  banner: Optional[str]
  abilities: List[Ability]