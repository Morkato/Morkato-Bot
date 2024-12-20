from __future__ import annotations
from .utils import NoNullDict
from .abc import Snowflake
from .flags import Flags
from .types import (
  User as UserPayload,
  HumanType,
  OniType,
  HybridType
)
from typing_extensions import Self
from typing import (
  TYPE_CHECKING,
  Optional,
  ClassVar
)
if TYPE_CHECKING:
  from .state import MorkatoConnectionState
  from .guild import Guild
class UserTypeFlags(Flags):
  HUMAN: int
  ONI: int
  HYBRID: int
  def human(self) -> bool: ...
  def oni(self) -> bool: ...
  def hybrid(self) -> bool: ...
class UserFlags(Flags):
  PRODIGY: int
  MARK: int
  BERSERK: int
  def prodigy(self) -> bool: ...
  def mark(self) -> bool: ...
  def berserk(self) -> bool: ...
class User:
  HUMAN: ClassVar[HumanType] = "HUMAN"
  ONI: ClassVar[OniType] = "ONI"
  HYBRID: ClassVar[HybridType] = "HYBRID"
  def __init__(self, state: MorkatoConnectionState, guild: Guild, payload: UserPayload) -> None:
    self.state = state
    self.http  = state.http
    self.guild = guild
    self.id = int(payload["id"])
    self.from_payload(payload)
  def from_payload(self, payload: UserPayload) -> None:
    self.type = payload["type"]
    self.flags = UserFlags(payload["flags"])
    self.ability_roll = payload["ability_roll"]
    self.family_roll = payload["family_roll"]
    self.prodigy_roll = payload["prodigy_roll"]
    self.mark_roll = payload["mark_roll"]
    self.berserk_roll = payload["berserk_roll"]
    self.abilities_id = [int(id) for id in payload["abilities"]]
    self.families_id = [int(id) for id in payload["families"]]
  async def update(
    self, *,
    flags: Optional[int] = None,
    ability_roll: Optional[int] = None,
    family_roll: Optional[int] = None,
    prodigy_roll: Optional[int] = None,
    mark_roll: Optional[int] = None,
    berserk_roll: Optional[int] = None
  ) -> Self:
    kwargs = NoNullDict(
      flags = flags,
      ability_roll = ability_roll,
      family_roll = family_roll,
      prodigy_roll = prodigy_roll,
      mark_roll = mark_roll,
      berserk_roll = berserk_roll
    )
    if kwargs:
      payload = await self.http.update_user(self.guild.id, self.id, **kwargs)
      self.from_payload(payload)
    return self
  async def sync_ability(self, ability: Snowflake) -> None:
    await self.http.registry_user_ability(self.guild.id, self.id, ability.id)
    self.abilities_id.append(ability.id)