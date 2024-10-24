from __future__ import annotations
from datetime import datetime
from .utils import (CircularDict, NoNullDict, DATE_FORMAT)
from .ability import Ability
from .family import Family
from .abc import Snowflake
from .player import Player
from .npc import Npc
from .attack import Attack
from .art import Art
from .types import (
  Guild as GuildPayload,
  AbilityType,
  NpcType,
  ArtType
)
from typing_extensions import Self
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
    self.start_rpg_calendar = datetime.strptime(payload["start_rpg_calendar"], DATE_FORMAT)
    self.start_rpg_date = datetime.strptime(payload["start_rpg_date"], DATE_FORMAT)
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
  def now(self) -> datetime:
    addition = datetime.now() - self.start_rpg_date
    return self.start_rpg_calendar + addition
  async def update(
    self, *,
    human_initial_life: Optional[int] = None,
    oni_initial_life: Optional[int] = None,
    hybrid_initial_life: Optional[int] = None,
    breath_initial: Optional[int] = None,
    blood_initial: Optional[int] = None,
    family_roll: Optional[int] = None,
    ability_roll: Optional[int] = None,
    roll_category_id: Optional[str] = None,
    off_category_id: Optional[str] = None
  ) -> Self:
    kwargs = NoNullDict(
      human_initial_life = human_initial_life,
      oni_initial_life = oni_initial_life,
      hybrid_initial_life = hybrid_initial_life,
      breath_initial = breath_initial,
      blood_initial = blood_initial,
      family_roll = family_roll,
      ability_roll = ability_roll,
      roll_category_id = roll_category_id,
      off_category_id = off_category_id
    )
    if kwargs:
      payload = await self.http.update_guild(self.id, **kwargs)
      self.from_payload(payload)
    return self
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
    ability_ids = (int(id) for id in payload["abilities"])
    for ability_id in ability_ids:
      ability = self.abilities.get(ability_id)
      if ability is None:
        raise RuntimeError
      npc._abilities[ability.id] = ability
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
  async def create_player(
    self, user: Snowflake, npc_kind: NpcType, *,
    ability_roll: Optional[int] = None,
    family_roll: Optional[int] = None,
    prodigy_roll: Optional[int] = None,
    mark_roll: Optional[int] = None,
    berserk_roll: Optional[int] = None,
    flags: Optional[SupportsInt] = None
  ) -> Player:
    payload = await self.http.create_player(
      self.id, user.id,
      npc_kind = npc_kind,
      ability_roll = ability_roll,
      family_roll = family_roll,
      prodigy_roll = prodigy_roll,
      mark_roll = mark_roll,
      berserk_roll = berserk_roll,
      flags = flags
    )
    player = Player(self.state, self, payload)
    self._add_player(player)
    return player
  async def create_ability(
    self, name: str, percent: int, npc_kind: SupportsInt, *,
    energy: Optional[int] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> Ability:
    payload = await self.http.create_ability(
      self.id,
      name = name,
      energy = energy,
      percent = percent,
      npc_kind = npc_kind,
      description = description,
      banner = banner
    )
    ability = Ability(self.state, self, payload)
    self.abilities.add(ability)
    return ability
  async def create_family(
    self, name: str, *,
    npc_type: int,
    percent: Optional[int] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> Family:
    payload = await self.http.create_family(
      self.id,
      name = name,
      percent = percent,
      npc_type = npc_type,
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