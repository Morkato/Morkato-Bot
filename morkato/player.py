from __future__ import annotations
from .npc import (Npc, NpcFlags)
from .utils import NoNullDict
from typing_extensions import Self
from typing import (
  TYPE_CHECKING,
  SupportsInt,
  Optional,
  Dict
)
if TYPE_CHECKING:
  from .state import MorkatoConnectionState
  from .ability import Ability
  from .family import Family
  from .abc import Snowflake
  from .guild import Guild
  from .types import (
    Player as PlayerPayload,
    NpcType
  )

class Player:
  def __init__(self, state: MorkatoConnectionState, guild: Guild, payload: PlayerPayload) -> None:
    self.state = state
    self.http = state.http
    self.guild = guild
    self.id = int(payload["id"])
    self.family: Optional[Family] = None
    self.npc: Optional[Npc] = None
    self.npc_type = payload["npc_type"]
    self.from_payload(payload)
    self.clear()
  def from_payload(self, payload: PlayerPayload) -> None:
    self.ability_roll = payload["ability_roll"]
    self.family_roll = payload["family_roll"]
    self.prodigy_roll = payload["prodigy_roll"]
    self.mark_roll = payload["mark_roll"]
    self.berserk_roll = payload["berserk_roll"]
    self.flags = NpcFlags(payload["flags"])
    self.family_id = int(payload["family_id"]) if payload["family_id"] is not None else None
    if self.family is None and self.family_id is not None:
      self.family = self.guild.families.get(self.family_id)
      if self.family is None:
        raise RuntimeError("Family ID: %s don't exists in this context." % self.family_id)
    if self.npc is None and payload["npc"] is not None:
      self.npc = Npc(self.state, self.guild, self.family, payload["npc"])
  def clear(self) -> None:
    self._abilities: Dict[int, Ability] = {}
    self._families: Dict[int, Family] = {}
  def already_registered(self) -> bool:
    return self.npc is not None
  def has_family(self, family: Snowflake, /) -> bool:
    return family.id in self._families.keys()
  def has_ability(self, ability: Snowflake, /) -> bool:
    return ability.id in self._abilities.keys()
  async def sync_family(self, family: Family) -> None:
    await self.http.sync_player_family(self.guild.id, self.id, family.id)
    self._families[family.id] = family
    self.family_roll -= 1
  async def sync_ability(self, ability: Ability, /) -> None:
    await self.http.sync_player_ability(self.guild.id, self.id, ability.id)
    self._abilities[ability.id] = ability
    self.ability_roll -= 1
  async def registry(self, name: str, surname: str, *, icon: Optional[str] = None) -> Npc:
    payload = await self.http.registry_player(self.guild.id, self.id, name=name, surname=surname, icon=icon)
    self.from_payload(payload)
    if self.npc is None:
      raise RuntimeError
    self.npc._abilities.update(self._abilities)
    return self.npc
  async def update(
    self, *,
    ability_roll: Optional[int] = None,
    family_roll: Optional[int] = None,
    family: Optional[Snowflake] = None,
    prodigy_roll: Optional[int] = None,
    mark_roll: Optional[int] = None,
    berserk_roll: Optional[int] = None,
    flags: Optional[SupportsInt] = None
  ) -> Self:
    payload = NoNullDict(
      ability_roll=ability_roll,
      family_roll=family_roll,
      family_id=family.id if family is not None else None,
      prodigy_roll = prodigy_roll,
      mark_roll = mark_roll,
      berserk_roll = berserk_roll,
      flags = flags
    )
    if payload:
      payload = await self.http.update_player(self.guild.id, self.id, **payload)
      self.from_payload(payload)
    return self
  async def delete(self) -> Self:
    payload = await self.http.delete_player(self.guild.id, self.id)
    self.guild._players.pop(self.id, None)
    self.from_payload(payload)
    return self