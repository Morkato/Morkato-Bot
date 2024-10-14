from __future__ import annotations
from .utils import (NoNullDict, extract_datetime_from_snowflake)
from datetime import datetime
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

class NpcFlags:
  PRODIGY = (1 << 1)
  MARK = (1 << 2)
  BERSERK = (1 << 3)
  def __init__(self, initial: SupportsInt = 0) -> None:
    self.__value = int(initial)
  def __repr__(self) -> str:
    return repr(self.__value)
  def __int__(self) -> int:
    return self.__value
  def copy(self) -> NpcFlags:
    return NpcFlags(int(self.__value))
  def has_intent(self, intent: int) -> bool:
    return (self.__value & intent) != 0
  def is_empty(self) -> bool:
    return self.__value == 0
  def set(self, intent: int) -> None:
    self.__value |= intent
  @property
  def prodigy(self) -> bool:
    return self.has_intent(self.PRODIGY)
  @property
  def mark(self) -> bool:
    return self.has_intent(self.MARK)
  @property
  def berserk(self) -> bool:
    return self.has_intent(self.BERSERK)
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
    self.energy = payload["energy"]
    self.flags = NpcFlags(payload["flags"])
    self.max_life = payload["max_life"]
    self.max_breath = payload["max_breath"]
    self.max_blood = payload["max_blood"]
    self.current_life = payload["current_life"]
    self.current_breath = payload["current_breath"]
    self.current_blood = payload["current_blood"]
  def clear(self) -> None:
    self._abilities: Dict[int, Ability] = {}
  @property
  def created_at(self) -> datetime:
    return extract_datetime_from_snowflake(self)
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