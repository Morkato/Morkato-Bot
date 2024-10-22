from __future__ import annotations
from .utils import NoNullDict, extract_datetime_from_snowflake
from .flags import Flags
from typing_extensions import Self
from datetime import datetime
from typing import (
  TYPE_CHECKING,
  SupportsInt,
  Optional
)
if TYPE_CHECKING:
  from .types import Attack as AttackPayload
  from .state import MorkatoConnectionState
  from .guild import Guild
  from .art import Art
class AttackFlags(Flags):
  UNAVOIDABLE: int
  INDEFENSIBLE: int
  AREA: int
  NOT_COUNTER_ATTACKABLE: int
  COUNTER_ATTACKABLE: int
  DEFENSIVE: int
  def unavoidable(self) -> bool: ...
  def indefensible(self) -> bool: ...
  def area(self) -> bool: ...
  def not_counter_attackable(self) -> bool: ...
  def counter_attackable(self) -> bool: ...
  def defensive(self) -> bool: ...
class Attack:
  def __init__(self, state: MorkatoConnectionState, guild: Guild, art: Art, payload: AttackPayload) -> None:
    self.state = state
    self.http = state.http
    self.guild = guild
    self.art = art
    self.id = int(payload["id"])
    self.from_payload(payload)
  def from_payload(self, payload: AttackPayload) -> None:
    self.name = payload["name"]
    self.name_prefix_art = payload["name_prefix_art"]
    self.description = payload["description"]
    self.banner = payload["banner"]
    self.damage = payload["damage"]
    self.breath = payload["breath"]
    self.blood = payload["blood"]
    self.flags = AttackFlags(payload["flags"])
  @property
  def created_at(self) -> datetime:
    return extract_datetime_from_snowflake(self)
  @property
  def updated_at(self) -> Optional[datetime]:
    if self._updated_at is not None:
      return datetime.fromtimestamp(self._updated_at / 1000.0)
    return None
  async def update(
    self, *,
    name: Optional[str] = None,
    name_prefix_art: Optional[str] = None,
    description: Optional[str] = None,
    resume_description: Optional[str] = None,
    banner: Optional[str] = None,
    damage: Optional[int] = None,
    breath: Optional[int] = None,
    blood: Optional[int] = None,
    flags: Optional[SupportsInt] = None
  ) -> Self:
    kwargs = NoNullDict(
      name=name,
      name_prefix_art=name_prefix_art,
      description=description,
      resume_description=resume_description,
      banner=banner,
      damage=damage,
      breath=breath,
      blood=blood,
      flags=flags
    )
    if kwargs:
      payload = await self.http.update_attack(self.guild.id, self.id, **kwargs)
      self.from_payload(payload)
    return self
  async def delete(self) -> Self:
    payload = await self.http.delete_attack(self.guild.id, self.id)
    self.from_payload(payload)
    self.art._del_attack(self)
    return self