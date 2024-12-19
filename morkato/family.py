from __future__ import annotations
from .user import UserTypeFlags
from .utils import NoNullDict
from typing_extensions import Self
from typing import (
  TYPE_CHECKING,
  SupportsInt,
  Optional,
  Dict
)
if TYPE_CHECKING:
  from .types import (
    Family as FamilyPayload,
    NpcType
  )
  from .state import MorkatoConnectionState
  from .ability import Ability
  from .abc import Snowflake
  from .guild import Guild

class Family:
  def __init__(self, state: MorkatoConnectionState, guild: Guild, payload: FamilyPayload) -> None:
    self.state = state
    self.http = state.http
    self.guild = guild
    self.id = int(payload["id"])
    self.from_payload(payload)
  def from_payload(self, payload: FamilyPayload) -> None:
    self.name = payload["name"]
    self.percent = payload["percent"]
    self.user_type = UserTypeFlags(payload["user_type"])
    self.description = payload["description"]
    self.banner = payload["banner"]
  async def update(
    self, *,
    name: Optional[str] = None,
    npc_type: Optional[SupportsInt] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> Self:
    payload = NoNullDict(
      name=name,
      npc_type=npc_type,
      description=description,
      banner=banner
    )
    if payload:
      payload = await self.http.update_family(self.guild.id, self.id, **payload)
      self.from_payload(payload)
    return self
  async def delete(self) -> Self:
    payload = await self.http.delete_family(self.guild.id, self.id)
    self.from_payload(payload)
    self.guild.families.remove(self)
    return self