from __future__ import annotations
from datetime import datetime
from .utils import (NoNullDict, extract_datetime_from_snowflake)
from .flags import Flags
from .types import (
  Npc as NpcPayload,
  HumanType,
  NpcType,
  OniType,
  HybridType
)
from typing_extensions import Self
from typing import (
  TYPE_CHECKING,
  SupportsInt,
  Optional,
  ClassVar,
  Dict
)
if TYPE_CHECKING:
  from .state import MorkatoConnectionState
  from .ability import Ability
  from .family import Family
  from .guild import Guild

class NpcFlags(Flags):
  PRODIGY: int
  MARK: int
  BERSERK: int
  def prodigy(self) -> bool: ...
  def mark(self) -> bool: ...
  def berserk(self) -> bool: ...
class Npc:
  HUMAN: ClassVar[HumanType] = "HUMAN"
  ONI: ClassVar[OniType] = "ONI"
  HYBRID: ClassVar[HybridType] = "HYBRID"
  def __init__(self, state: MorkatoConnectionState, guild: Guild, family: Family, payload: NpcPayload) -> None:
    self.state = state
    self.http = state.http
    self.family = family
    self.guild = guild
    self.id = int(payload["id"])
    self.from_payload(payload)
    self.clear()
  def from_payload(self, payload: NpcPayload) -> None:
    self.name = payload["name"]
    self.surname = payload["surname"]
    self.type = payload["type"]
    self.icon = payload["icon"]
    self.max_energy = payload["max_energy"]
    self.energy = payload["energy"]
    self.flags = NpcFlags(payload["flags"])
    self.max_life = payload["max_life"]
    self.max_breath = payload["max_breath"]
    self.max_blood = payload["max_blood"]
    self.current_life = payload["current_life"]
    self.current_breath = payload["current_breath"]
    self.current_blood = payload["current_blood"]
    self.last_action = datetime.fromtimestamp(payload["last_action"] / 1000.0)
  def clear(self) -> None:
    self._abilities: Dict[int, Ability] = {}
  @property
  def created_at(self) -> datetime:
    return extract_datetime_from_snowflake(self)
  @property
  def max_energy(self) -> int:
    return 100 + sum(ability.energy for ability in self._abilities.values())
  async def update(
    self, *,
    name: Optional[str] = None,
    surname: Optional[str] = None,
    flags: Optional[SupportsInt] = None,
    type: Optional[NpcType] = None,
    max_life: Optional[int] = None,
    max_breath: Optional[int] = None,
    max_blood: Optional[int] = None,
    current_life: Optional[int] = None,
    current_breath: Optional[int] = None,
    current_blood: Optional[int] = None,
    icon: Optional[str] = None
  ) -> Self:
    kwargs = NoNullDict(
      name = name,
      surname = surname,
      flags = flags,
      type = type,
      max_life = max_life,
      max_breath = max_breath,
      max_blood = max_blood,
      current_life = current_life,
      current_breath = current_breath,
      current_blood = current_blood,
      icon = icon
    )
    if kwargs:
      payload = await self.http.update_npc(self.guild.id, self.id, **kwargs)
      self.from_payload(payload)
    return self