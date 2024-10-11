from __future__ import annotations
from .utils import (CircularDict, NoNullDict)
from typing_extensions import Self
from .npc import Npc
from typing import (
  TYPE_CHECKING,
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
    self.clear()
  def _add_ability(self, ability: Ability) -> None:
    self._abilities[ability.id] = ability
  def _del_ability(self, ability: Snowflake) -> None:
    self._abilities.pop(ability.id, None)
  def _add_npc(self, npc: Npc) -> None:
    self._npcs[npc.id] = npc
    self.guild._npcs[npc.id] = npc
  def _del_npc(self, npc: Npc) -> None:
    self._npcs.pop(npc.id, None)
    self.guild._npcs.pop(npc.id, None)
  def from_payload(self, payload: FamilyPayload) -> None:
    self.name = payload["name"]
    self.percent = payload["percent"]
    self.npc_kind = payload["npc_kind"]
    self.description = payload["description"]
    self.banner = payload["banner"]
  def clear(self) -> None:
    self._abilities: Dict[int, Ability] = {}
    self._npcs: CircularDict[int, Npc] = CircularDict(128)
  def get_ability(self, id: int, /) -> Optional[Ability]:
    return self._abilities.get(id)
  async def create_npc(
    self, name: str, surname: str, type: NpcType, *,
    icon: Optional[str] = None
  ) -> Npc:
    payload = await self.http.create_npc(
      self.guild.id, self.id,
      name=name,
      surname=surname,
      type=type,
      icon=icon
    )
    npc = Npc(self.state, self.guild, self, payload)
    self._add_npc(npc)
    return npc
  async def sync_ability(self, ability: Ability) -> None:
    await self.http.sync_family_ability(self.guild.id, self.id, ability.id)
    self._add_ability(ability)
  async def update(
    self, *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> Self:
    payload = NoNullDict(
      name=name,
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