from __future__ import annotations
from typing_extensions import Self
from .utils import NoNullDict
from typing import (
  TYPE_CHECKING,
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
    self.guild = guild
    self.id = int(payload["id"])
    self.from_payload(payload)
  def from_payload(self, payload: AbilityPayload) -> None:
    self.name = payload["name"]
    self.type = payload["type"]
    self.percent = payload["percent"]
    self.npc_kind = payload["npc_kind"]
    self.immutable = payload["immutable"]
    self.description = payload["description"]
    self.banner = payload["banner"]
  async def update(
    self, *,
    name: Optional[str] = None,
    type: Optional[AbilityType] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> Self:
    payload = NoNullDict(
      name=name,
      type=type,
      description=description,
      banner=banner
    )
    if not payload:
      return self
    payload = await self.state.update_ability(self.guild.id, self.id, **payload)
    self.from_payload(payload)
    return self
  async def delete(self) -> Self:
    payload = await self.state.delete_ability(self.guild.id, self.id)
    self.from_payload(payload)
    self.guild._del_ability(self)
    for family in self.guild._families.values():
      family._del_ability(self)
    return self