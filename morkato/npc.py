from __future__ import annotations
from .utils import extract_datetime_from_snowflake
from datetime import datetime
from .types import (
  Npc as NpcPayload
)
from typing import (
  TYPE_CHECKING,
  Optional
)
if TYPE_CHECKING:
  from .state import MorkatoConnectionState
  from .family import Family
  from .guild import Guild

class Npc:
  def __init__(self, state: MorkatoConnectionState, guild: Guild, family: Family, payload: NpcPayload) -> None:
    self.state = state
    self.http = state.http
    self.family = family
    self.guild = guild
    self.id = int(payload["id"])
    self.from_payload(payload)
  def from_payload(self, payload: NpcPayload) -> None:
    self.name = payload["name"]
    self.surname = payload["surname"]
    self.icon = payload["type"]
    self.energy = payload["energy"]
    self.max_life = payload["max_life"]
    self.max_breath = payload["max_breath"]
    self.max_blood = payload["max_blood"]
    self.current_life = payload["current_life"]
    self.current_breath = payload["current_breath"]
    self.current_blood = payload["current_blood"]
  @property
  def created_at(self) -> datetime:
    return extract_datetime_from_snowflake(self)