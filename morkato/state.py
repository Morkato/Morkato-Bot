from __future__ import annotations

from typing import (
  Callable,
  TYPE_CHECKING,
  Literal,
  TypeVar,
  Union,
  List,
  Dict,
  Any
)

if TYPE_CHECKING:
  from .gateway import MorkatoWebSocket
  from .http import HTTPClient
  from .bot import MorkatoBotBase

  from .types.item      import Item as TypeItem, PlayerItem as TypePlayerItem
  from .types.player    import Player as TypePlayer
  from .types.attack    import Attack as TypeAttack
  from .types.guild     import Guild as TypeGuild
  from .types.art       import Art as TypeArt
  from .abc import Snowflake

  EditEvent = Dict[Literal['before', 'after'], 'T']

from .attack import ArtAttack, ItemAttack
from .item import PlayerItem, Item
from .object import Object
from .player import Player
from .guild import Guild
from .art import Art

import logging
import inspect

logger = logging.getLogger(__name__)
T = TypeVar('T')

class MorkatoConnectionState:
  if TYPE_CHECKING:
    _get_bot: Callable[..., MorkatoBotBase]
    _get_websocket: Callable[..., MorkatoWebSocket]
    _parsers: Callable[..., None]

  def __init__(
    self, *,
    dispatch: Callable[..., Any],
    http: HTTPClient,
    **kwargs
  ) -> None:
    self.http: HTTPClient = http
    self.dispatch: Callable[..., Any] = dispatch

    self.parsers: Dict[str, Callable[[Any], None]]
    self.parsers = parsers = {}
    for attr, func in inspect.getmembers(self):
      if attr.startswith('parse_'):
        logger.info("Prepare Parser (%s)", attr[6:].upper())
        parsers[attr[6:].upper()] = func

    self.clear()
  
  def __repr__(self) -> str:
    return f'<{self.__class__.__name__} token={self.http.token!r} http>'
  
  def clear(self) -> None:
    self.guilds: Dict[int, Guild] = {  }
  
  def _get_guild(self, id: int) -> Union[Guild, None]:
    return self.guilds.get(id)
  
  def _add_guild(self, guild: Guild, /) -> None:
    self.guilds[guild.id] = guild
  
  def _remove_guild(self, guild: Snowflake) -> None:
    del self.guilds[guild.id]

  def parse_raw_create_guild(self, raw_guild_payload: TypeGuild) -> None:
    for guild_payload in raw_guild_payload:
      self.parse_create_guild(guild_payload, raw=True)
      
  def parse_create_guild(self, guild_payload: TypeGuild, *, raw: bool = False) -> None:
    guild = Guild(self, guild_payload)

    self._add_guild(guild)

    self.dispatch('guild', guild)
  
  def parse_delete_guild(self, guild_payload: TypeGuild) -> None:
    guild = Object(id=int(guild_payload['id']))

    try:
      self._remove_guild(guild)
    except (KeyError, IndexError):
      logger.info("Ignoring delete for guild ID: %s", guild_payload['id'])
  
  def parse_raw_create_art(self, raw_art_payload: list[TypeArt]) -> None:
    for art_payload in raw_art_payload:
      self.parse_create_art(art_payload, raw=True)

  def parse_create_art(self, art_payload: TypeArt, *, raw: bool = False) -> None:
    guild_id = int(art_payload['guild_id'])

    guild = self._get_guild(guild_id)
    if guild is None:
      logger.warn("Ignoring art why guild (ID:%s) not found", guild_id)
      
      return

    art = Art(self, guild, art_payload)

    if not raw:
      logger.info('Art (%s): %s for guild: %s has created.', art.id, art.name, guild.id)

    guild._add_art(art)

    self.dispatch('art', art)

  def parse_update_art(self, edit: EditEvent[TypeArt]) -> None:
    guild_id = int(edit['before']['guild_id'])

    guild = self._get_guild(guild_id)
    if guild is None:
      logger.warn("Ignoring art edit why guild (ID:%s) not found", guild_id)
      
      return
    
    art_id = int(edit['before']['id'])
    
    after = guild.get_art(art_id)
    if after is None:
      logger.warn("Ignoring art edit why art (ID:%s) not found in guild (ID:%s)", art_id, art_id)

      return
    
    before = Art(self, guild, edit['before'])
    after._load_variables(edit['after'])

    self.dispatch('art_edit', before, after)
  
  def parse_delete_art(self, delete: TypeArt) -> None:
    guild_id = int(delete['guild_id'])

    guild = self._get_guild(guild_id)
    if guild is None:
      logger.warn("Ignoring art delete why guild (ID:%s) not found", guild_id)
      
      return
    
    art_id = int(delete['id'])
    
    try:
      art = guild._remove_art(Object(id=art_id))

      logger.info("Art (%s): %s of guild: %s has deleted.", art.name, art.id, guild.id)
      
      self.dispatch('art_delete', art)
    except (KeyError, IndexError):
      logger.warn("Ignoring art delete: %s why art not found in guild: %s", art_id, guild.id)
  
  def parse_raw_create_player(self, raw: List[TypePlayer]) -> None:
    for player in raw:
      self.parse_create_player(player, raw=True)

  def parse_create_player(self, create: TypePlayer, *, raw: bool = False) -> None:
    guild_id = int(create['guild_id'])

    guild = self._get_guild(guild_id)

    if guild is None:
      logger.warn("Ignoring create player(%s): %s for guild: %s.", create['name'], create['id'], guild_id)
      
      return
    
    player = Player(self, guild, create)

    guild._add_player(player)

    if not raw:
      logger.info("Create player (%s): %s on guild: %s.", player._name, player._id, guild._id)

    self.dispatch('player', player)
  
  def parse_update_player(self, edit: EditEvent[Player]) -> None:
    guild_id = int(edit['before']['guild_id'])

    guild = self._get_guild(guild_id)

    if guild is None:
      logger.warn("Ignoring edit player: %s for guild: %s.", edit['before']['id'], guild_id)
      
      return
    
    before = Player(self, guild, edit['before'])
    after = guild._get_player(before)

    if after is None:
      logger.warn("Ignoring edit player: %s for guild: %s.", before._id, guild_id)

      return
    
    after._load_variables(edit['after'])

    logger.info("Update player (%s): %s on guild: %s.", before._name, before._id, guild._id)

    self.dispatch('player_edit', before, after)
  
  def parse_delete_player(self, delete: TypePlayer) -> None:
    guild_id = int(delete['guild_id'])

    guild = self._get_guild(guild_id)

    if guild is None:
      logger.warn("Ignoring delete player: %s for guild: %s.", delete['id'], guild_id)
      
      return
    
    try:
      player = guild._remove_player(Object(id=int(delete['id'])))

      self.dispatch('player_delete', player)
    except (KeyError, IndexError):
      logger.warn("Ignoring delete player: %s for guild: %s.", delete['id'], guild_id)
  
  def parse_raw_create_item(self, raw: List[TypeItem]) -> None:
    for item in raw:
      self.parse_create_item(item, raw=True)
  
  def parse_create_item(self, create: TypeItem, *, raw: bool = False) -> None:
    guild_id = int(create['guild_id'])

    guild = self._get_guild(guild_id)

    if guild is None:
      logger.warn("Ignoring create item: %s for guild: %s.", create['id'], guild_id)
      
      return
    
    item = Item(self, guild, create)

    guild._add_item(item)

    if not raw:
      logger.info("Create a new item (%s): %s for guild: %s.", item._name, item._id, guild._id)
    
      self.dispatch('item', item)

      return
    
    self.dispatch('raw_item', item)
  
  def parse_update_item(self, edit: EditEvent[TypeItem]) -> None:
    guild_id = int(edit['before']['guild_id'])

    guild = self._get_guild(guild_id)

    if guild is None:
      logger.warn("Ignoring edit item: %s for guild: %s.", edit['before']['id'], guild_id)
      
      return
    
    before = Item(self, guild, edit['before'])
    after = guild._get_item_by_id(before._id)

    if after is None:
      logger.warn("Ignoring edit item: %s for guild: %s.", before._id, guild_id)

      return
    
    after._load_variables(edit['after'])

    logger.info("Update player (%s): %s on guild: %s.", before._name, before._id, guild._id)

    self.dispatch('player_edit', before, after)
  
  def parse_delete_item(self, delete: TypeItem) -> None:
    guild_id = int(delete['guild_id'])

    guild = self._get_guild(guild_id)

    if guild is None:
      logger.warn("Ignoring delete item: %s for guild: %s.", delete['id'], guild_id)
      
      return
    
    try:
      item = guild._remove_item(Object(id=int(delete['id'])))

      self.dispatch('item_delete', item)
    except (KeyError, IndexError):
      logger.warn("Ignoring delete item: %s for guild: %s.", delete['id'], guild_id)
  
  def parse_raw_create_attack(self, raw: List[TypeAttack]) -> None:
    for attack in raw:
      self.parse_create_attack(attack, raw=True)
  
  def parse_create_attack(self, create: TypeAttack, *, raw: bool = False) -> None:
    guild_id = int(create['guild_id'])

    guild = self._get_guild(guild_id)
    
    if (not create['art_id'] and not create['item_id']) or guild is None:
      logger.warn("Ignoring create attack(%s): %s for guild: %s.", create['name'], create['id'], guild_id)

      return
    
    item_or_art = guild._get_art_by_id(int(create['art_id'])) if create['art_id'] is not None else guild._get_item_by_id(int(create['item_id']))

    if item_or_art is None:
      logger.warn("Ignoring create attack(%s): %s for guild: %s.", create['name'], create['id'], guild_id)

      return
    
    attack = ArtAttack(self, item_or_art, create) if isinstance(item_or_art, Art) else ItemAttack(self, item_or_art, create)

    if not raw:
      logger.info("Create attack (%s): %s on guild: %s.", attack._name, attack._id, guild._id)
    
    item_or_art._add_attack(attack)

    self.dispatch('attack', attack)
  
  def parse_raw_player_inventory(self, raw: List[TypePlayerItem]) -> None:
    for chunk in raw:
      self.parse_inventory_player_item_add(chunk, raw=True)
  
  def parse_inventory_player_item_add(self, create: TypePlayerItem, *, raw: bool = False) -> None:
    guild_id = int(create['guild_id'])
    item_id = int(create['item_id'])
    player_id = int(create['player_id'])

    guild = self._get_guild(guild_id)

    if guild is None:
      # Logging ...

      return
    
    player = guild._get_player(player_id)
    item = guild._get_item_by_id(item_id)

    if player is None or item is None:
      # Logging ...

      return

    player_item = PlayerItem(self, player, item, create)

    if not raw:
      # Logging ...

      return
    
    player._add_item(player_item)

    self.dispatch('player_item_add', player_item)
