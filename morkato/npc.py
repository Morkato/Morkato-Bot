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
  from .guild import Guild

class Npc:
  def __init__(self, state: MorkatoConnectionState, guild: Guild, payload: NpcPayload) -> None:
    self.state = state
    self.guild = guild
    self.id = int(payload["id"])
    self.from_payload(payload)
  def from_payload(self, payload: NpcPayload) -> None:
    self.family_id: Optional[str] = None
    self.name = payload["name"]
    self.surname = payload["surname"]
    self.icon = payload["type"]
    self.energy = payload["energy"]
    if payload.get("family_id") is not None and self.family_id is None:
      self.family_id = int(payload["family_id"])
    self.max_life = payload["max_life"]
    self.max_breath = payload["max_breath"]
    self.max_blood = payload["max_blood"]
    self.current_life = payload["current_life"]
    self.current_breath = payload["current_breath"]
    self.current_blood = payload["current_blood"]
  @property
  def created_at(self) -> datetime:
    return extract_datetime_from_snowflake(self)