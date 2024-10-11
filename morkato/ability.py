from __future__ import annotations
from typing_extensions import Self
from .utils import NoNullDict
from typing import (
  TYPE_CHECKING,
  SupportsInt,
  Optional,
  Tuple
)
if TYPE_CHECKING:
  from .types import (
    Ability as AbilityPayload,
    AbilityType
  )
  from .state import MorkatoConnectionState
  from .guild import Guild
class AbilityIntents:
  HUMAN = (1 << 1)
  ONI = (1 << 2)
  HYBRID = (1 << 3)
  ALL_INTENTS: Tuple[int] = (HUMAN, ONI, HYBRID)
  def __init__(self, initial: SupportsInt = 0) -> None:
    self.__value = int(initial)
  def __repr__(self) -> str:
    return repr(self.__value)
  def __int__(self) -> int:
    return self.__value
  def has_intent(self, intent: int) -> bool:
    if not intent in self.ALL_INTENTS:
      return False
    return (self.__value & intent) != 0
  def is_empty(self) -> bool:
    return self.__value == 0
  def set(self, intent: int) -> None:
    self.__value |= intent
  @property
  def human(self) -> bool:
    return (self.__value & self.HUMAN) != 0
  @property
  def oni(self) -> bool:
    return (self.__value & self.ONI) != 0
  @property
  def hybrid(self) -> bool:
    return (self.__value & self.HYBRID) != 0
class Ability:
  def __init__(self, state: MorkatoConnectionState, guild: Guild, payload: AbilityPayload) -> None:
    self.state = state
    self.http = state.http
    self.guild = guild
    self.id = int(payload["id"])
    self.from_payload(payload)
  def from_payload(self, payload: AbilityPayload) -> None:
    self.name = payload["name"]
    self.type = payload["type"]
    self.percent = payload["percent"]
    self.npc_kind = AbilityIntents(payload["npc_kind"])
    self.immutable = payload["immutable"]
    self.description = payload["description"]
    self.banner = payload["banner"]
  async def update(
    self, *,
    name: Optional[str] = None,
    type: Optional[AbilityType] = None,
    npc_kind: Optional[SupportsInt] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> Self:
    payload = NoNullDict(
      name=name,
      type=type,
      npc_kind=npc_kind,
      description=description,
      banner=banner
    )
    if not payload:
      return self
    payload = await self.http.update_ability(self.guild.id, self.id, **payload)
    self.from_payload(payload)
    return self
  async def delete(self) -> Self:
    payload = await self.http.delete_ability(self.guild.id, self.id)
    self.from_payload(payload)
    self.guild.abilities.remove(self)
    for family in self.guild.families:
      family._del_ability(self)
    return self