from __future__ import annotations

from typing import Generator, Union, overload, TYPE_CHECKING, Set, Any

if TYPE_CHECKING:
  from .client import MorkatoClientManager
  from .types  import Guild as TypeGuild

  import discord

from .attack import (
  ParentAttack,
  ArtAttack,
  Attack
)

from .player import Player
from .item   import Item
from .art    import Art

from datetime import datetime
from .        import errors, utils

class Guild:
  ITEMS: Set[Guild] = set()

  @staticmethod
  def create(client: MorkatoClientManager, payload: TypeGuild) -> Guild:
    id = int(payload['id'])

    guild = utils.get(Guild.ITEMS, lambda g: g._id == id)

    if guild:
      return guild
    
    guild = Guild(client, payload)

    Guild.ITEMS.add(guild)

    return guild

  def __init__(
    self,
    client:  MorkatoClientManager,
    payload: TypeGuild
  ) -> None:
    self.client = client

    self._players = utils.Players(self)
    self._attacks = utils.Attacks(self)
    self._arts    = utils.Arts(self)
    self._items   = utils.Items(self)

    self._morkato_origin: Union[discord.Guild, None] = None

    self._load_variables(payload)

  def __hash__(self) -> int:
    return hash(self._id)

  def __repr__(self) -> str:
    return f'<Guild id={self._id}>'
  
  def _load_variables(self, payload: TypeGuild) -> None:
    self._id = int(payload['id'])

    self._created_at = datetime.strptime(payload['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    self._updated_at = datetime.strptime(payload['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
  
  def get_all_arts(self) -> Generator[Art, Any, None]:
    for art in Art.ITEMS:
      if art._guild_id != self._id:
        continue

      setattr(art, '_morkato_guild', self)
      
      yield art
  
  def get_all_items(self) -> Generator[Item, Any, None]:
    for item in Item.ITEMS:
      if item._guild_id != self._id:
        continue

      setattr(item, '_morkato_guild', self)

      yield item
  
  def _get_art_by_id(self, id: int) -> Art:
    result = Art.get(self, id)

    if not result:
      raise errors.NotFoundError("Essa arte (Respiração, Kekkijutsu ou Estilo de Luta) não existe")
    
    return result
  
  def _get_art_by_name(self, name: str) -> Art:
    fmt = lambda text: utils.strip_text(text,
      ignore_accents=True,
      ignore_empty=True,
      case_insensitive=True,
      strip_text=True
    )

    name = fmt(name)

    result = utils.get(self.get_all_arts(), lambda art: fmt(art.name) == name)

    if not result:
      raise errors.NotFoundError("Essa arte (Respiração, Kekkijutsu ou Estilo de Luta) não existe")
    
    return result
  
  def _get_item_by_id(self, id: int) -> Item:
    result = Item.get(self, id)

    if not result:
      raise errors.NotFoundError("Esse item não existe.")
    
    return result
  
  def get_art(self, obj: Union[str, int]) -> Art:
    if isinstance(obj, int):
      return self._get_art_by_id(obj)
    
    elif isinstance(obj, str):
      return self._get_art_by_name(obj)
    
    raise TypeError
  
  def get_item(self, obj: Union[str, int]) -> Item:
    return self._items.get(obj)
  
  @overload
  def get_attack(self, id: int, /) -> Attack: ...
  @overload
  def get_attack(self, name: str, /) -> Union[ArtAttack, ParentAttack]: ...
  @overload
  def get_attack(self, msg: discord.Message, /) -> Union[ArtAttack, ParentAttack]: ...
  def get_attack(self, obj: Union[discord.Message, str, int], /) -> Attack:
    return self._attacks.get(obj)
  
  def get_player(self, obj: Union[discord.Member, int]) -> Player:
    return self._players.get(obj)
  
  @property
  def origin(self) -> discord.Guild:
    if not self._morkato_origin:
      self._morkato_origin = self.client.get_guild(self._id)

      if not self._morkato_origin:
        raise Exception
    
    if self._morkato_origin.id != self.id:
      self._morkato_origin = None

      return self.origin
    
    return self._morkato_origin
  
  @property
  def id(self) -> int:
    return self._id
  
  @property
  def created_at(self) -> datetime:
    return self._created_at
  
  @property
  def updated_at(self) -> datetime:
    return self._updated_at
  
  @property
  def arts(self) -> utils.Arts:
    return self._arts
  
  @property
  def items(self) -> utils.Items:
    return self._items
  
  @property
  def attacks(self) -> utils.Attacks:
    return self._attacks
  
  @property
  def players(self) -> utils.Players:
    return self._players
  