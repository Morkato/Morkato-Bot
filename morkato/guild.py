from __future__ import annotations
from .utils import (UnresolvedSnowflakeListImpl, CircularDict)
from .abc import (UnresolvedSnowflakeList, Snowflake)
from .ability import Ability
from .family import Family
from .attack import Attack
from .user import User
from .art import Art
from .types import (
  Guild as GuildPayload,
  UserType,
  ArtType
)
from typing import (
  TYPE_CHECKING,
  SupportsInt,
  Optional,
  TypeVar,
  Dict
)
if TYPE_CHECKING:
  from .state import MorkatoConnectionState

T = TypeVar('T', bound='Snowflake')
class Guild:
  def __init__(self, state: MorkatoConnectionState, id: int, payload: GuildPayload) -> None:
    self.state = state
    self.http = state.http
    self.id = id
    self.from_payload(payload)
    self.clear()
  def from_payload(self, payload: GuildPayload) -> None:
    self.human_initial_life = payload["human_initial_life"]
    self.oni_initial_life = payload["oni_initial_life"]
    self.hybrid_initial_life = payload["hybrid_initial_life"]
    self.breath_initial = payload["breath_initial"]
    self.blood_initial = payload["blood_initial"]
    self.roll_category_id = int(payload["roll_category_id"]) if payload["roll_category_id"] is not None else None
    self.off_category_id = int(payload["off_category_id"]) if payload["off_category_id"] is not None else None
  def clear(self) -> None:
    self.abilities_percent = 0
    self.families_percent = 0
    self._attacks: Dict[int, Attack] = {}
    self._users: CircularDict[int, User] = CircularDict(128)

    self.arts: UnresolvedSnowflakeList[Art] = UnresolvedArtList(self.state, self)
    self.abilities: UnresolvedSnowflakeList[Ability] = UnresolvedAbilityList(self.state, self)
    self.families: UnresolvedSnowflakeList[Family] = UnresolvedFamilyList(self.state, self)
  def get_cached_user(self, id: int) -> Optional[User]:
    return self._users.get(id)
  async def fetch_user(self, id: int) -> User:
    payload = await self.http.fetch_user(self.id, id)
    user = User(self.state, self, payload)
    self._users[user.id] = user
    return user
  def get_attack(self, id: int) -> Optional[Attack]:
    return self._attacks.get(id)
  async def create_user(
    self, id: int, *,
    type: UserType,
    flags: Optional[int] = None,
    ability_roll: Optional[int] = None,
    family_roll: Optional[int] = None,
    prodigy_roll: Optional[int] = None,
    mark_roll: Optional[int] = None,
    berserk_roll: Optional[int] = None
  ) -> User:
    payload = await self.http.create_user(
      self.id, id,
      type = type,
      flags = flags,
      ability_roll = ability_roll,
      family_roll = family_roll,
      prodigy_roll = prodigy_roll,
      mark_roll = mark_roll,
      berserk_roll = berserk_roll
    )
    user = User(self.state, self, payload)
    self._users[user.id] = user
    return user
  async def create_art(
    self, name: str, type: ArtType, *,
    energy: Optional[int] = None,
    life: Optional[int] = None,
    breath: Optional[int] = None,
    blood: Optional[int] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> Art:
    payload = await self.http.create_art(
      self.id,
      name = name,
      type = type,
      energy = energy,
      life = life,
      breath = breath,
      blood = blood,
      description = description,
      banner = banner
    )
    art = Art(self.state, self, payload)
    self.arts.add(art)
    return art
  async def create_ability(
    self, name: str, *,
    percent: Optional[int] = None,
    user_type: Optional[SupportsInt] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> Ability:
    payload = await self.http.create_ability(
      self.id,
      name = name,
      percent = percent,
      user_type = user_type,
      description = description,
      banner = banner
    )
    ability = Ability(self.state, self, payload)
    self.abilities.add(ability)
    return ability
  async def create_family(
    self, name: str, *,
    user_type: SupportsInt,
    percent: Optional[int] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> Family:
    payload = await self.http.create_family(
      self.id,
      name = name,
      percent = percent,
      user_type = user_type,
      description = description,
      banner = banner
    )
    family = Family(self.state, self, payload)
    self.families.add(family)
    return family
class UnresolvedObjectListImpl(UnresolvedSnowflakeListImpl[T]):
  def __init__(self, state: MorkatoConnectionState, guild: Guild) -> None:
    super().__init__()
    self.state = state
    self.http = state.http
    self.guild = guild
class UnresolvedArtList(UnresolvedObjectListImpl[Art]):
  async def resolve_impl(self) -> None:
    guild = self.guild
    http = self.http
    state = self.state
    payload = await http.fetch_arts(guild.id)
    for art_data in payload:
      art = Art(state, guild, art_data)
      attack_datas = art_data["attacks"]
      for attack_data in attack_datas:
        attack = Attack(state, guild, art, attack_data)
        art._add_attack(attack)
      self.add(art)
class UnresolvedAbilityList(UnresolvedObjectListImpl[Ability]):
  async def resolve_impl(self) -> None:
    guild = self.guild
    state = self.state
    http = self.http
    payload = await http.fetch_abilities(guild.id)
    for ability_data in payload:
      ability = Ability(state, guild, ability_data)
      self.add(ability)
  def add(self, object: Ability, /) -> None:
    if self.already_loaded():
      super().add(object)
      self.guild.abilities_percent += object.percent
  def remove(self, object: Snowflake, /) -> Optional[Ability]:
    if not self.already_loaded():
      return None
    ability = super().remove(object)
    if ability is not None:
      self.guild.abilities_percent -= ability.percent
    return ability
class UnresolvedFamilyList(UnresolvedObjectListImpl[Family]):
  async def resolve_impl(self) -> None:
    guild = self.guild
    state = self.state
    http = self.http
    abilities = guild.abilities
    payload = await http.fetch_families(guild.id)
    await abilities.resolve()
    for family_data in payload:
      family = Family(state, guild, family_data)
      self.add(family)
  def add(self, object: Family, /) -> None:
    if self.already_loaded():
      super().add(object)
      self.guild.families_percent += object.percent
  def remove(self, object: Snowflake, /) -> Optional[Family]:
    if not self.already_loaded():
      return None
    family = super().remove(object)
    if family is not None:
      self.guild.families_percent -= family.percent
    return family