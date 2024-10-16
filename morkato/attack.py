from __future__ import annotations
from .utils import NoNullDict, extract_datetime_from_snowflake
from typing_extensions import Self
from datetime import datetime
from typing import (
  TYPE_CHECKING,
  SupportsInt,
  Optional,
  Tuple
)
if TYPE_CHECKING:
  from .types import Attack as AttackPayload
  from .state import MorkatoConnectionState
  from .guild import Guild
  from .art import Art
class AttackIntents:
  UNAVOIDABLE = (1 << 2)
  INDEFENSIBLE = (1 << 3)
  AREA = (1 << 4)
  NOT_COUNTER_ATTACKABLE = (1 << 5)
  COUNTER_ATTACKABLE = (1 << 6)
  DEFENSIVE = (1 << 7)
  @classmethod
  def all(cls) -> AttackIntents:
    intents = cls()
    intents.set(cls.UNAVOIDABLE)
    intents.set(cls.INDEFENSIBLE)
    intents.set(cls.AREA)
    intents.set(cls.NOT_COUNTER_ATTACKABLE)
    intents.set(cls.COUNTER_ATTACKABLE)
    intents.set(cls.DEFENSIVE)
    return intents
  def __init__(self, initial: SupportsInt = 0) -> None:
    self.__value = int(initial)
  def __repr__(self) -> str:
    return repr(self.__value)
  def __int__(self) -> int:
    return self.__value
  def copy(self) -> AttackIntents:
    return AttackIntents(int(self.__value))
  def has_intent(self, intent: int) -> bool:
    return (self.__value & intent) != 0
  def is_empty(self) -> bool:
    return self.__value == 0
  def set(self, intent: int) -> None:
    self.__value |= intent
  @property
  def unavoidable(self) -> bool:
    return self.has_intent(self.UNAVOIDABLE)
  @property
  def indefensible(self) -> bool:
    return self.has_intent(self.INDEFENSIBLE)
  @property
  def area(self) -> bool:
    return self.has_intent(self.AREA)
  @property
  def not_counter_attackable(self) -> bool:
    return self.has_intent(self.NOT_COUNTER_ATTACKABLE)
  @property
  def counter_attackable(self) -> bool:
    return self.has_intent(self.COUNTER_ATTACKABLE)
  @property
  def defensive(self) -> bool:
    return self.has_intent(self.DEFENSIVE)
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
    self.intents = AttackIntents(payload["intents"])
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
    intents: Optional[AttackIntents] = None
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
      intents=intents
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