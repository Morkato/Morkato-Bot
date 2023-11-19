from __future__ import annotations

from typing_extensions import Self
from typing            import (
  Optional,
  NoReturn,
  Union,
  
  TYPE_CHECKING,
  Set
)

from numerize.numerize import numerize as num_fmt
from .errors           import NotFoundError
from .                 import utils

if TYPE_CHECKING:
  from .client import MorkatoClientManager

  from .utils.abc import Snowflake
  from .player_item import PlayerItem as TypePlayerItem
  from .player      import Player
  from .item        import Item
  from .guild       import Guild

from datetime import datetime

class PlayerItem:
  ITEMS: Set[PlayerItem] = set()

  @staticmethod
  def get(guild: Union[Snowflake, int], player: Union[Snowflake, int], item: Union[Snowflake, int]) -> Union[PlayerItem, None]:
    guild_id = guild if isinstance(guild, int) else guild.id
    player_id = player if isinstance(player, int) else player.id
    item_id = item if isinstance(item, int) else item.id
    
    unique = hash((guild_id, player_id, item_id))

    return utils.get(PlayerItem.ITEMS, lambda pi: hash(pi) == unique)
  
  @staticmethod
  def create(client: MorkatoClientManager, payload: TypePlayerItem) -> PlayerItem:
    item = PlayerItem.get(int(payload['guild_id']), int(payload['player_id']), int(payload['item_id']))

    if not item:
      item = PlayerItem(client, payload)

      PlayerItem.ITEMS.add(item)
    
    return item

  def __init__(self, client: MorkatoClientManager, data: TypePlayerItem) -> None:
    self._client = client

    self._morkato_guild: Union[Guild, None] = None # type: ignore
    self._morkato_player: Union[Player, None] = None # type: ignore
    self._morkato_item: Union[Item, None] = None # type: ignore
    
    self._load_variables(data)

  def __repr__(self) -> str:
    return f'<PlayerItem player{self.player.name!r} item={self.item.name!r} stack={self._stack}>'
  
  def __hash__(self) -> int:
    return hash((self._guild_id, self._player_id, self._item_id))
  
  def _load_variables(self, payload: TypePlayerItem) -> None:
    self._guild_id  = int(payload['guild_id'])
    self._player_id = int(payload['player_id'])
    self._item_id   = int(payload['item_id'])

    self._stack = payload['stack']
    
    self._created_at = datetime.fromtimestamp(payload['created_at'] / 1000)
  
  @property
  def guild(self) -> Guild:
    if not self._morkato_guild:
      self._morkato_guild = self._client.get_morkato_guild(self._guild_id)
    
    if not self._morkato_guild.id == self._guild_id:
      self._morkato_guild = None

      return self.guild
    
    return self._morkato_guild
  
  @property
  def player(self) -> Player:
    if not self._morkato_player:
      self._morkato_player = self.guild.get_player(self._player_id)
    
    if not self._morkato_player.id == self._player_id:
      self._morkato_player = None

      return self.player
    
    return self._morkato_player
  
  @property
  def item(self) -> Player:
    if not self._morkato_item:
      self._morkato_item = self.guild.get_item(self._item_id)
    
    if not self._morkato_item.id == self._item_id:
      self._morkato_item = None

      return self.item
    
    return self._morkato_item