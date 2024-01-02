from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  Optional,
  Union,
  List,
  Dict,
  overload
)

if TYPE_CHECKING:
  from .types.guild import Guild as TypeGuild
  from .abc import Snowflake
  
  from .http import HTTPClient
  from .state import MorkatoConnectionState

  from .attack import ItemAttack, ArtAttack, Attack
  from .player import Player
  from .art import ArtType
  from .item import Item

from .art import Art

from .errors.guild import ManyItemAttackError
from .errors import ErrorType, geterr
from itertools import chain
from .http import Route
from .utils.etc import (
  find,
  fmt,
  get
)

class Guild:
  def __init__(self, state: MorkatoConnectionState, payload: TypeGuild) -> None:
    self.state = state
    
    self._load_variables(payload)
    self.clear()
  
  def _load_variables(self, payload: TypeGuild) -> None:
    self._id = int(payload['id'])

    self._created_at = payload['created_at']
    self._updated_at = payload['updated_at']
  
  def clear(self) -> None:
    self._players: Dict[int, Player] = {  }
    self._items: Dict[int, Item] = {  }
    self._arts: Dict[int, Art] = {  }
    self._attacks: Dict[int, Attack] = {  }

  @property
  def id(self) -> int:
    return self._id

  @property
  def players(self) -> List[Player]:
    return sorted(self._players.values(), key=lambda player: (player._life + player._breath + player._blood) // 3)
  
  @property
  def arts(self) -> List[Art]:
    return sorted(self._arts.values(), key=lambda art: art.id)
  
  def _get_http(self) -> HTTPClient:
    return self.state.http
  
  def _get_art_by_name(self, name: str) -> Union[Art, None]:
    text_fmt = fmt

    name = text_fmt(name)

    return get(self._arts.values(), lambda art: text_fmt(art.name) == name)
  
  def _get_art_by_id(self, id: int) -> Union[Art, None]:
    return self._arts.get(id)
  
  def _get_player(self, obj: Union[Snowflake, int]) -> Union[Player, None]:
    return self._players.get(obj if isinstance(obj, int) else obj.id)
  
  def _get_item_by_name(self, name: str) -> Union[Item, None]:
    text_fmt = fmt

    name = text_fmt(name)

    return get(self._items.values(), lambda item: text_fmt(item._name) == name)

  def _get_item_by_id(self, id: int) -> Union[Item, None]:
    return self._items.get(id)
  
  def _get_attack_by_id(self, id: int) -> Union[Attack, None]:
    return self._attacks.get(id)
  
  def _get_item_attack_by_name_if_unknown_item(self, name: str) -> Union[ItemAttack, None]:
    text_fmt = fmt

    name = text_fmt(name)

    attacks = chain(*(item._attacks.values() for item in self._items.values()))
    attacks = list(find(attacks, lambda attack: text_fmt(attack.name) == name))

    if not attacks:
      return
    
    if len(attacks) != 1:
      raise ManyItemAttackError(attacks)
    
    return attacks[0]

  def _get_item_attack_by_name(self, name: str) -> Union[ItemAttack, None]:
    if not ':' in name:
      return self._get_item_attack_by_name_if_unknown_item(name)
    
    item_name, name = name.split(':', 1)
    item = self.get_item(item_name)
    
    return item.get_attack(name)
  
  def _get_attack_by_name(self, name: str) -> Union[ArtAttack, ItemAttack, None]:
    if ':' in name:
      return self._get_item_attack_by_name(name)
    
    text_fmt = fmt

    name = text_fmt(name)
    attacks = chain(*(art._attacks.values() for art in self._arts.values()))

    result = get(attacks, lambda attack: text_fmt(attack._name) == name)

    if result is None:
      result = self._get_item_attack_by_name_if_unknown_item(name)

    return result
  
  def get_art(self, id: Union[str, int]) -> Art:
    result = self._get_art_by_name(id) if isinstance(id, str) else self._get_art_by_id(id)

    if not result:
      raise geterr(ErrorType.ART_NOTFOUND)
    
    return result

  def get_item(self, id_or_name: Union[str, int]) -> Item:
    result = self._get_item_by_name(id_or_name) if isinstance(id_or_name, str) else self._get_item_by_id(id_or_name)

    if not result:
      raise geterr(ErrorType.ITEM_NOTFOUND)
    
    return result
  
  def get_player(self, obj: Union[Snowflake, int]) -> Player:
    result = self._get_player(obj)

    if not result:
      raise geterr(ErrorType.PLAYER_NOTFOUND)
    
    return result

  @overload
  def get_attack(self, id: int) -> Attack: ...
  @overload
  def get_attack(self, name: str) -> Union[ItemAttack, ArtAttack]: ...
  def get_attack(self, name_or_id: Union[str, int]) -> Attack:
    result = self._get_attack_by_name(name_or_id) if isinstance(name_or_id, str) else self._get_attack_by_id(name_or_id)

    if result is None:
      raise geterr(ErrorType.ATTACK_NOTFOUND)
    
    return result
  
  def _add_art(self, art: Art) -> None:
    self._arts[art._id] = art
  
  def _add_player(self, player: Player) -> None:
    self._players[player._id] = player
  
  def _add_item(self, item: Item) -> None:
    self._items[item.id] = item
  
  def _remove_art(self, art: Snowflake) -> Art:
    return self._arts.pop(art.id)
  
  def _remove_player(self, player: Snowflake) -> Player:
    return self._players.pop(player.id)

  def _remove_item(self, item: Snowflake) -> Item:
    return self._items.pop(item.id)
  
  async def create_art(
    self, *,
    name:              str,
    type:              ArtType,
    embed_title:       Optional[str] = None,
    embed_description: Optional[str] = None,
    embed_url:         Optional[str] = None
  ) -> Art:
    http = self._get_http()

    payload = { "name": name, "type": type }

    if embed_title is not None:
      payload['embed_title'] = embed_title
    
    if embed_description is not None:
      payload['embed_description'] = embed_description
    
    if embed_url is not None:
      payload['embed_url'] = embed_url
    
    data = await http.request(Route('POST', '/arts/{gid}', gid=self.id), json=payload)

    return Art(self.state, self, data)