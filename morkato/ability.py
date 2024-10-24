from __future__ import annotations
from typing_extensions import Self
from .utils import NoNullDict
from .flags import Flags
from typing import (
  TYPE_CHECKING,
  SupportsInt,
  Optional
)
if TYPE_CHECKING:
  from .types import (
    Ability as AbilityPayload,
    AbilityType
  )
  from .state import MorkatoConnectionState
  from .guild import Guild
class AbilityFlags(Flags):
  HUMAN = (1 << 1)
  ONI = (1 << 2)
  HYBRID = (1 << 3)
  def human(self) -> bool: ...
  def oni(self) -> bool: ...
  def hybrid(self) -> bool: ...
class Ability:
  def __init__(self, state: MorkatoConnectionState, guild: Guild, payload: AbilityPayload) -> None:
    self.state = state
    self.http = state.http
    self.guild = guild
    self.id = int(payload["id"])
    self.from_payload(payload)
  def from_payload(self, payload: AbilityPayload) -> None:
    self.name = payload["name"]
    self.energy = payload["energy"]
    self.percent = payload["percent"]
    self.npc_type = AbilityFlags(payload["npc_type"])
    self.description = payload["description"]
    self.banner = payload["banner"]
  async def update(
    self, *,
    name: Optional[str] = None,
    type: Optional[AbilityType] = None,
    energy: Optional[int] = None,
    npc_kind: Optional[SupportsInt] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> Self:
    payload = NoNullDict(
      name=name,
      type=type,
      energy = energy,
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