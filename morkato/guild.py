from __future__ import annotations
from .utils import CircularDict
from .ability import Ability
from .family import Family
from .abc import Snowflake
from .player import Player
from .npc import Npc
from .art import Art
from .types import (
  Guild as GuildPayload,
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
    self._npcs: CircularDict[int, Npc] = CircularDict(128)
    self._players: CircularDict[int, Player] = CircularDict(128)
    self._attacks: Dict[int, Attack] = {}

    self.arts: LazyGuildObjectListProtocol[Art] = LazyArtList(self.state, self)
    self.abilities: LazyGuildObjectListProtocol[Ability] = LazyAbilityList(self.state, self)
    self.families: LazyGuildObjectListProtocol[Family] = LazyFamilyList(self.state, self)
  def _add_npc(self, npc: Npc) -> None:
    self._npcs[npc.id] = npc
  def _add_player(self, player: Player) -> None:
    self._players[player.id] = player
  def get_attack(self, id: int) -> Optional[Attack]:
    return self._attacks.get(id)
  def get_cached_npc(self, id: Union[str, int]) -> Optional[Npc]:
    return self._npcs.get(id)
  def get_cached_player(self, id: int) -> Optional[Player]:
    return self._players.get(id)
  async def fetch_npc(self, id: Union[str, int]) -> Npc:
    payload = await self.http.fetch_npc(self.id, id)
    npc = Npc(self.state, self, payload)
    self._add_npc(npc)
    return npc
  async def fetch_player(self, id: int) -> Player:
    if not self.families.already_loaded():
      await self.families.resolve()
    payload = await self.http.fetch_player(self.id, id)
    player = Player(self.state, self, payload)
    for family_id in payload["families"]:
      family = self.families.get(int(family_id))
      if family is None:
        raise RuntimeError
      player._families[family.id] = family
    for ability_id in payload["abilities"]:
      ability = self.abilities.get(int(ability_id))
      if ability is None:
        raise RuntimeError
      player._abilities[ability.id] = ability
    self._add_player(player)
    return player
  async def create_art(
    self, name: str, type: ArtType, *,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> Art:
    payload = await self.http.create_art(
      self.id,
      name = name,
      type = type,
      description = description,
      banner = banner
    )
    art = Art(self.state, self, payload)
    self.arts.add(art)
    return art
  async def create_player(
    self, user: Snowflake, npc_kind: NpcType, *,
    ability_roll: Optional[int] = None,
    family_roll: Optional[int] = None,
    is_prodigy: Optional[bool] = None,
    has_mark: Optional[bool] = None
  ) -> Player:
    payload = await self.http.create_player(
      self.id, user.id,
      npc_kind = npc_kind,
      ability_roll = ability_roll,
      family_roll = family_roll,
      is_prodigy = is_prodigy,
      has_mark = has_mark
    )
    player = Player(self.state, self, payload)
    self._add_player(player)
    return player
  async def create_ability(
    self, name: str, type: AbilityType, percent: int, npc_kind: SupportsInt, *,
    immutable: Optional[bool] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> Ability:
    payload = await self.http.create_ability(
      self.id,
      name = name,
      type = type,
      percent = percent,
      npc_kind = npc_kind,
      immutable = immutable,
      description = description,
      banner = banner
    )
    ability = Ability(self.state, self, payload)
    self.abilities.add(ability)
    return ability
  async def create_family(
    self, name: str, *,
    npc_kind: NpcType,
    percent: Optional[int] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> Family:
    payload = await self.http.create_family(
      self.id,
      name = name,
      percent = percent,
      npc_kind = npc_kind,
      description = description,
      banner = banner
    )
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
    http = self.state.http
    payload = await http.fetch_arts(self.guild.id)
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
    http = state.http
    payload = await http.fetch_abilities(guild.id)
    for ability_data in payload:
      ability = Ability(state, guild, ability_data)
      self.add(ability)
    self._already_loaded = True
  def add(self, object: Ability, /) -> None:
    super().add(object)
    self.guild.abilities_percent += object.percent
  def remove(self, object: Snowflake, /) -> Optional[Ability]:
    ability = super().remove(object)
    if ability is not None:
      self.guild.abilities_percent -= ability.percent
    return ability
class LazyFamilyList(LazyGuildObjectList[Family]):
  async def resolve(self) -> None:
    guild = self.guild
    state = self.state
    http = state.http
    abilities = guild.abilities
    if not abilities.already_loaded():
      await abilities.resolve()
    payload = await http.fetch_families(guild.id)
    for family_data in payload:
      family = Family(state, guild, family_data)
      ability_ids = family_data["abilities"]
      for ability_id in ability_ids:
        ability = abilities.get(int(ability_id))
        if ability is None:
          raise RuntimeError("Unknown ability reference: %s for family: %s (Guild ID: %s)" % (ability_id, family.id, guild.id))
        family._add_ability(ability)
      self.add(family)
    self._already_loaded = True
  def add(self, object: Family, /) -> None:
    super().add(object)
    self.guild.families_percent += object.percent
  def remove(self, object: Snowflake, /) -> Optional[Family]:
    family = super().remove(object)
    if family is not None:
      self.guild.families_percent -= family.percent
    return family