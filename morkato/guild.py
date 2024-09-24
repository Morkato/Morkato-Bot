from __future__ import annotations
from .utils import CircularDict
from .ability import Ability
from .family import Family
from .abc import Snowflake
from .npc import Npc
from .art import Art
from .types import (
  AbilityType,
  NpcType,
  ArtType
)
from typing import (
  TYPE_CHECKING,
  SupportsInt,
  Iterator,
  Optional,
  Protocol,
  TypeVar,
  Union,
  Dict,
  List
)
if TYPE_CHECKING:
  from .state import MorkatoConnectionState
  from .attack import Attack

T = TypeVar('T', bound='Snowflake')
class Guild:
  def __init__(self, state: MorkatoConnectionState, id: int) -> None:
    self.state = state
    self.id = id
    self.clear()
  def clear(self) -> None:
    self.abilities_percent = 0
    self._npcs: CircularDict[int, Npc] = CircularDict(8)
    self._attacks: Dict[int, Attack] = {}

    self.arts: LazyGuildObjectListProtocol[Art] = LazyArtList(self.state, self)
    self.abilities: LazyGuildObjectListProtocol[Ability] = LazyAbilityList(self.state, self)
    self.families: LazyGuildObjectListProtocol[Family] = LazyFamilyList(self.state, self)
  def _add_npc(self, npc: Npc) -> None:
    self._npcs[npc.id] = npc
  def get_attack(self, id: int) -> Optional[Attack]:
    return self._attacks.get(id)
  def get_cached_npc(self, id: Union[str, int]) -> Optional[Npc]:
    return self._npcs.get(id)
  async def fetch_npc(self, id: Union[str, int]) -> Npc:
    payload = await self.state.fetch_npc(self.id, id)
    npc = Npc(self.state, self, payload)
    self._add_npc(npc)
    return npc
  async def create_art(self, name: str, type: ArtType, *, description: Optional[str] = None, banner: Optional[str] = None) -> Art:
    payload = await self.state.create_art(self.id, name=name, type=type, description=description, banner=banner)
    art = Art(self.state, self, payload)
    self.arts.add(art)
    return art
  async def create_npc(self, name: str, surname: str, type: NpcType, *, family: Optional[Snowflake] = None, icon: Optional[str] = None) -> Npc:
    family_id = family.id if family is not None else None
    payload = await self.state.create_npc(self.id, name=name, surname=surname, type=type, family_id=family_id, icon=icon)
    npc = Npc(self.state, self, payload)
    self._add_npc(npc)
    return npc
  async def create_ability(self, name: str, type: AbilityType, percent: int, npc_kind: SupportsInt, *, immutable: Optional[bool] = None, description: Optional[str] = None, banner: Optional[str] = None) -> Ability:
    payload = await self.state.create_ability(self.id, name=name, type=type, percent=percent, npc_kind=npc_kind, immutable=immutable, description=description, banner=banner)
    ability = Ability(self.state, self, payload)
    self.abilities.add(ability)
    return ability
  async def create_family(self, name: str, *, description: Optional[str] = None, banner: Optional[str] = None) -> Family:
    payload = await self.state.create_family(self.id, name=name, description=description, banner=banner)
    family = Family(self.state, self, payload)
    self.families.add(family)
    return family
class LazyGuildObjectListProtocol(Protocol[T]):
  def __iter__(self) -> Iterator[T]: ...
  def __len__(self) -> int: ...
  def order(self) -> List[T]: ...
  def already_loaded() -> bool: ...
  async def resolve() -> None: ...
  def add(self, object: T, /) -> None: ...
  def remove(self, object: Snowflake, /) -> Optional[T]: ...
  def get(self, id: int) -> Optional[T]: ...
class LazyGuildObjectList(LazyGuildObjectListProtocol[T]):
  def __init__(self, state: MorkatoConnectionState, guild: Guild) -> None:
    self.state = state
    self.guild = guild
    self.items: Dict[int, T] = {}
    self._already_loaded = False
  def __iter__(self) -> Iterator[T]:
    return iter(self.items.values())
  def __len__(self) -> int:
    return len(self.items)
  def order(self) -> List[T]:
    return sorted(self, key=lambda item: item.id)
  def already_loaded(self) -> bool:
    return self._already_loaded
  async def resolve(self) -> None:
    raise NotImplementedError
  def add(self, object: T, /) -> None:
    self.items[object.id] = object
  def remove(self, object: Snowflake, /) -> Optional[T]:
    return self.items.pop(object.id, None)
  def get(self, id: int, /) -> T:
    return self.items.get(id)
class LazyArtList(LazyGuildObjectList[Art]):
  async def resolve(self) -> None:
    payload = await self.state.fetch_arts(self.guild.id)
    for art_data in payload:
      art = Art(self.state, self.guild, art_data)
      attack_datas = art_data["attacks"]
      for attack_data in attack_datas:
        attack = Attack(self.state, self.guild, art, attack_data)
        art._add_attack(attack)
      self.add(art)
    self._already_loaded = True
class LazyAbilityList(LazyGuildObjectList[Ability]):
  async def resolve(self) -> None:
    guild = self.guild
    state = self.state
    payload = await state.fetch_abilities(guild.id)
    for ability_data in payload:
      ability = Ability(state, guild, ability_data)
      self.add(ability)
    self._already_loaded = True
  def add(self, object: Ability, /) -> None:
    super().add(object)
    self.guild.abilities_percent += object.percent
  def remove(self, object: Snowflake, /) -> Optional[T]:
    ability = super().remove(object)
    if ability is not None:
      self.guild.abilities_percent -= ability.percent
    return ability
class LazyFamilyList(LazyGuildObjectList[Family]):
  async def resolve(self) -> None:
    guild = self.guild
    state = self.state
    abilities = guild.abilities
    if not abilities.already_loaded():
      await abilities.resolve()
    payload = await state.fetch_families(guild.id)
    for family_data in payload:
      family = Family(state, guild, family_data)
      ability_ids = map(lambda ability: int(ability["id"]), family_data["abilities"])
      for ability_id in ability_ids:
        ability = abilities.get(ability_id)
        if ability is None:
          raise RuntimeError("Unknown ability reference: %s for family: %s (Guild ID: %s)" % (ability_id, family.id, guild.id))
        family._add_ability(ability)
      self.add(family)
    self._already_loaded = True