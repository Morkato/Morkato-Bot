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
class Guild(TypedDict):
  human_initial_life: int
  oni_initial_life: int
  hybrid_initial_life: int
  breath_initial: int
  blood_initial: int
  family_roll: int
  ability_roll: int
  start_rpg_date: str
  start_rpg_calendar: str
  roll_category_id: Optional[str]
  off_category_id: Optional[str]
class Art(TypedDict):
  name: str
  guild_id: str
  id: str
  type: ArtType
  life: int
  breath: int
  blood: int
  energy: int
  description: Optional[str]
  banner: Optional[str]
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
  flags: int
class Npc(TypedDict):
  guild_id: str
  id: str
  name: str
  surname: str
  type: NpcType
  family_id: Optional[str]
  max_energy: int
  energy: int
  flags: int
  max_life: int
  max_breath: int
  max_blood: int
  current_life: int
  current_breath: int
  current_blood: int
  icon: Optional[str]
  abilities: List[str]
  last_action: Optional[int]
class Ability(TypedDict):
  guild_id: str
  id: str
  name: str
  type: AbilityType
  energy: int
  percent: int
  npc_kind: int
  immutable: bool
  description: Optional[str]
  banner: Optional[str]
class Family(TypedDict):
  guild_id: str
  id: str
  name: str
  percent: int
  npc_type: int
  description: Optional[str]
  banner: Optional[str]
  abilities: List[str]
class Player(TypedDict):
  guild_id: str
  id: str
  family_id: Optional[str]
  npc_type: NpcType
  npc: Optional[Npc]
  ability_roll: int
  family_roll: int
  prodigy_roll: int
  mark_roll: int
  berserk_roll: int
  flags: int