from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  
  Optional,
  Coroutine,
  Literal,
  Callable,
  TypeVar,
  Tuple,

  Dict,
  List,
  Any
)

if TYPE_CHECKING:
  from .gateway import MorkatoWebSocket

from .types import (
  Player as TypePlayer,
  Attack as TypeAttack,
  Guild  as TypeGuild,
  Art    as TypeArt,
  Item   as TypeItem
)

from .player import Player
from .attack import Attack
from .guild  import Guild
from .art    import Art
from .item   import Item

from . import errors

import inspect
import asyncio
import re

T = TypeVar('T')

EventEdit = Dict[Literal['before', 'after'], T]

class MorkatoDispatch:
  def __init__(self, ws: MorkatoWebSocket) -> None:
    self._ws = ws
    self._client = ws._client

    self._listeners: Dict[str, List[Tuple[asyncio.Future[Any], Callable[..., bool]]]] = {}

    self._parsers = {  }

    for name, attr in inspect.getmembers(self):
      if not name.startswith('parse_'): continue

      name = re.sub(r'^parse_', '', name).upper()
      
      self.debug(f'Prepare Parser (Event): ' + name)

      self._parsers[name] = attr

  def debug(self, msg: str, *, guild_id: Optional[int] = None) -> None:
    headers = ''

    if guild_id:
      headers += f'[Guild ID: {guild_id}] '

    headers += '[Dispatch] '

    print(headers + msg)

  def add_listener(self, ev: str, future: asyncio.Future[Any], check: Callable[..., bool]) -> None:
    try:
      listeners = self._listeners[ev]
    except KeyError:
      listeners = self._listeners[ev] = []
    finally:
      listeners.append((future, check))

  async def _handle_coro(self, coro: Callable[..., Coroutine[Any, Any, Any]], /, *args, **kwargs) -> None:
    try:
      await coro(*args, **kwargs)
    except Exception as err:
      await self._client.on_error(coro.__name__, err)

  def dispatch(self, e: str, *args, **kwargs) -> None:
    ev_name = 'on_morkato_' + e

    coro = getattr(self._client, ev_name, None)

    if coro:
      asyncio.create_task(self._handle_coro(coro, *args, **kwargs))
    
    listeners = None

    try:
      listeners = self._listeners[e]
    except KeyError:
      return
    
    removed = []
    length = len(args)

    for idx, (future, conn) in enumerate(listeners):
      if future.cancelled():
        removed.append(idx)

        continue

      try:
        result = conn(*args)

        if not result:
          continue
          
        if length == 0:
          future.set_result(None)
          
        elif length == 1:
          future.set_result(args[0])

        else:
          future.set_result(args)

        removed.append(idx)
      
      except Exception as err:
        future.set_exception(err)

    if len(listeners) == len(removed):
        self._listeners.pop(e)

        return
    
    for idx in reversed(removed):
      del listeners[idx]
  
  def __call__(self, e: str, d: Any) -> None:
    event = None
    
    try:
      event = self._parsers[e]
    except KeyError:
      self.debug('Unknown Dispatch: ' + e)

      return
    
    event(d)
  
  @property
  def guilds(self):
    return self._ws._guilds
  
  @property
  def arts(self):
    return self._ws._arts
  
  @property
  def items(self):
    return self._ws._items
  
  @property
  def attacks(self):
    return self._ws._attacks
  
  @property
  def players(self):
    return self._ws._players
  
  def parse_create_guild(self, data: TypeGuild):
    guild = Guild(client=self._client, payload=data)

    self.guilds.append(guild)

    self.dispatch('guild', guild)

  def parse_create_art(self, data: TypeArt):
    art = Art(client=self._client, payload=data)

    self.debug(f'Art ID: {art.id} ({art.name}) has created.', guild_id=art.guild_id)

    self.arts.append(art)

    self.dispatch('art', art)
  
  def parse_edit_art(self, data: EventEdit[TypeArt]):
    before = data['before']
    after = data['after']

    guild_id = int(before['guild_id'])
    id = int(before['id'])
    
    try:
      guild = self._client.get_morkato_guild(guild_id)
      art   = guild.get_art(id)

      before_art = Art(self._client, before)

      art._load_variables(after)

      self.debug(f'Art ID: {id} ({art.name}) has edited.', guild_id=guild_id)

      self.dispatch('art_edit', before_art, art)
    
    except errors.NotFoundError:
      self.debug(f'Art ID: {id} ignored edit.', guild_id=guild_id)
  
  def parse_delete_art(self, data: TypeArt):
    guild_id = int(data['guild_id'])
    id = int(data['id'])

    try:
      guild = self._client.get_morkato_guild(guild_id)
      art   = guild._arts.drop(id)

      self.debug(f'Art ID: {art.id} ({art.name}) has deleted.', guild_id=guild_id)

      self.dispatch('art_delete', art)
    
    except errors.NotFoundError:
      self.debug(f'Art ID: {id} ignored delete.', guild_id=guild_id)
  
  def parse_create_item(self, data: TypeItem) -> None:
    item = Item.create(client=self._client, payload=data)
  
    self.debug(f'Arm ID: {item.id} ({item.name}) has created.', guild_id=item.guild_id)

    self.dispatch('item', item)
  
  def parse_edit_item(self, data: EventEdit[TypeItem]) -> None:
    before = data['before']
    after = data['after']

    guild_id = int(before['guild_id'])
    id = int(before['id'])

    try:
      guild = self._client.get_morkato_guild(guild_id)
      item   = guild.get_item(id)

      before_item = Item(self._client, before)

      item._load_variables(after)

      self.dispatch('item_edit', before_item, item)

      self.debug(f'Item ID: {item.id} ({item.name}) has edited.', guild_id=guild_id)

    except errors.NotFoundError:
      self.debug(f'Item ID: {id} has ignored for edit.', guild_id=guild_id)
  
  def parse_delete_item(self, data: TypeItem) -> None:
    guild_id = int(data['guild_id'])
    id = int(data['id'])

    try:
      guild = self._client.get_morkato_guild(guild_id)
      item   = guild._items.drop(id)

      self.dispatch('item_delete', item)

      self.debug(f'Item ID: {id} ({item.name}) has deleted.', guild_id=guild_id)
    
    except errors.NotFoundError:
      self.debug(f'Item ID: {id} has ignored delete.')
  
  def parse_create_attack(self, data: TypeAttack) -> None:
    attack = Attack(client=self._client, payload=data)

    self.attacks.append(attack)

    self.dispatch('attack', attack)

    self.debug(f'Attack ID: {attack.id} ({attack.name}) has created.')

  def parse_edit_attack(self, data: EventEdit[TypeAttack]) -> None:
    before = data['before']
    after = data['after']

    guild_id = int(before['guild_id'])
    id = int(before['id'])
  
    try:
      guild  = self._client.get_morkato_guild(guild_id)
      attack = guild.get_attack(id)

      before_attack = Attack(self._client, before)

      attack._load_variables(after)

      self.dispatch('attack_edit', before_attack, attack)

      self.debug(f'Attack ID: {id} ({attack.name}) has edited.', guild_id=guild_id)
    
    except errors.NotFoundError:
      self.debug(f'Attack ID: {id} has ignored edited.', guild_id=guild_id)
  
  def parse_delete_attack(self, data: TypeAttack) -> None:
    guild_id = int(data['guild_id'])
    id = int(data['id'])

    try:
      guild  = self._client.get_morkato_guild(guild_id)
      attack = guild._attacks.drop(id)

      self.dispatch('attack_delete', attack)

      self.debug(f'Attack ID: {id} ({attack.name}) has deleted.', guild_id=guild_id)
    
    except:
      self.debug(f'Attack ID: {id} has ignored delete.', guild_id=guild_id)
    
  def parse_create_player(self, data: TypePlayer) -> None:
    player = Player(client=self._client, payload=data)

    self.players.append(player)

    self.dispatch('player', player)

    self.debug(f'Player ID: {player.id} ({player.name}) has created.', guild_id=player.guild_id)
  
  def parse_edit_player(self, data: EventEdit[TypePlayer]) -> None:
    before = data['before']
    after = data['after']

    guild_id = int(before['guild_id'])
    id = int(before['id'])

    try:
      guild  = self._client.get_morkato_guild(guild_id)
      player = guild.get_player(id)

      before_player = Player(self._client, before)
      
      player._load_variables(after)

      self.dispatch('player_edit', before_player, player)

      self.debug(f'Player ID {id} ({player.name}) has edited.', guild_id=guild_id)

    except errors.NotFoundError:
      self.debug(f'Player ID: {id} has ignored edit.', guild_id=guild_id)

  def parse_delete_player(self, data: TypePlayer) -> None:
    guild_id = int(data['guild_id'])
    id = int(data['id'])

    try:
      guild  = self._client.get_morkato_guild(guild_id)
      player = guild._players.drop(id)

      self.dispatch('player_delete', player)

      self.debug(f'Player ID: {id} ({player.name}) has deleted.', guild_id=guild_id)
    
    except errors.NotFoundError:
      self.debug(f'Player ID: {id} has ignored delete.', guild_id=guild_id)