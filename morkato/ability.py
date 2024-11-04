from __future__ import annotations
from typing_extensions import Self
from .utils import NoNullDict
from .npc import NpcTypeFlags
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
    self.npc_type = NpcTypeFlags(payload["npc_type"])
    self.description = payload["description"]
    self.banner = payload["banner"]
  async def update(
    self, *,
    name: Optional[str] = None,
    energy: Optional[int] = None,
    npc_type: Optional[SupportsInt] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> Self:
    payload = NoNullDict(
      name=name,
      energy = energy,
      npc_type=npc_type,
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