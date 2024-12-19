from __future__ import annotations
from .flags import Flags
from .types import (
  User as UserPayload
)
from typing import (
  TYPE_CHECKING
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
  