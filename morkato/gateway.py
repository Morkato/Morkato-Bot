from __future__ import annotations

from typing import (
  Literal,
  Callable,
  Optional,
  Union,
  Tuple,

  overload,
  
  TYPE_CHECKING,
  Set,
  Any
)

from itertools import zip_longest
from .dispatch import MorkatoDispatch

if TYPE_CHECKING:
  from .client  import MorkatoClientManager

from .player_item import PlayerItem
from .player import Player
from .attack import Attack
from .guild  import Guild
from .art    import Art
from .item   import Item
from .       import (
  utils
)

import datetime

import aiohttp
import asyncio

import time
import zlib
import yarl

import os

class WebSocketClosure(Exception):
  def __init__(self, type: Union[aiohttp.WSMsgType.CLOSE, aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSING], *args: object) -> None:
    super().__init__(*args)

    self.type = type

class MorkatoWebSocket:

  DISPATCH  = 0
  HEARTBEAT = 1
  IDENTIFY  = 2
  READY     = 3
  HELLO     = 4

  def __init__(
    self,
    client: MorkatoClientManager,
    socket: aiohttp.ClientWebSocketResponse, *,
    loop:   asyncio.AbstractEventLoop = utils.UNDEFINED
  ) -> None:
    self.socket = socket
    self.loop   = loop or asyncio.get_running_loop()

    self._client = client

    self._guilds:       Set[Guild]      = Guild.ITEMS
    self._players:      Set[Player]     = Player.ITEMS
    self._attacks:      Set[Attack]     = Attack.ITEMS
    self._arts:         Set[Art]        = Art.ITEMS
    self._items:        Set[Item]       = Item.ITEMS
    self._player_items: Set[PlayerItem] = PlayerItem.ITEMS
    
    self._dispatch = MorkatoDispatch(self)
    self._latency  = float('inf')
    
    self._zlib = zlib.decompressobj()
    self._buffer = bytearray()
  
  @classmethod
  async def from_client(cls, client: MorkatoClientManager, login: str, *, gateway: yarl.URL) -> MorkatoWebSocket:
    socket = await client._api.ws(gateway=gateway)

    self = cls(client, socket)

    await self.login(login)

    client._morkato_guilds = self._guilds
    client._players        = self._players
    client._attacks        = self._attacks
    client._arts           = self._arts
    client._items          = self._items
    client._player_items   = self._player_items

    return self

  async def login(self, login: str) -> None:
    await self.send(self.IDENTIFY, d=login)
  
  async def received_message(self, msg: Any, /) -> None:
    if type(msg) is bytes:
      self._buffer.extend(msg)

      if len(msg) < 4 or msg[-4:] != b'\x00\x00\xff\xff':
        return

      msg = self._zlib.decompress(self._buffer)
      msg = msg.decode('utf-8')
      
      self._buffer = bytearray()

    msg = utils.from_json(msg)

    e    = msg.get('e')
    op   = msg['op']
    data = msg['d']

    if op == self.DISPATCH and e:
      self._dispatch(e, data)
      
    elif op == self.HEARTBEAT:
      before = datetime.datetime.fromtimestamp(data / 1000)

      self._latency = time.time() - before.timestamp()

      await self.send(self.HEARTBEAT, d = int(datetime.datetime.now().timestamp() * 1000))

    elif op == self.READY:
      c = self._client
      
      for (guild, attack, player, art, item, player_item) in zip_longest(
        data['guilds'],
        data['attacks'],
        data['players'],
        data['arts'],
        data['items'],
        data['playerItems'],
        fillvalue=None
      ):
        if guild:
          Guild.create(c, guild)
        
        if attack:
          Attack.create(c, attack)
        
        if player:
          Player.create(c, player)

        if art:
          Art.create(c, art)
        
        if item:
          Item.create(c, item)
        
        if player_item:
          PlayerItem.create(c, player_item)
  
    elif op == self.HELLO:
      print(data)

  @property
  def latency(self) -> float:
    return self._latency

  @property
  def closed(self) -> bool:
    return self.socket.closed
  
  async def send(self, op: Literal[0, 1, 2, 3, 4], e: str = utils.UNDEFINED, d: Any = utils.UNDEFINED):
    payload = { "op": op }

    if utils.nis_undefined(e) and op == 0:
      payload['e'] = e

    if utils.nis_undefined(d):
      payload['d'] = d
    
    await self.socket.send_json(payload)

  async def poll_event(self, timeout: Optional[float] = None) -> Tuple[str, Any]:
    coro = self.socket.receive()

    msg = await (coro if not timeout else asyncio.wait_for(coro, timeout))

    if msg.type in (aiohttp.WSMsgType.TEXT, aiohttp.WSMsgType.BINARY):
      return await self.received_message(msg.data)
      
    elif msg.type == aiohttp.WSMsgType.ERROR:
      raise msg.data
      
    elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.CLOSING, aiohttp.WSMsgType.CLOSE):
      raise WebSocketClosure(msg.type)

  async def close(self) -> bool:
    return await self.socket.close()
  
  @overload
  async def wait_for(self,
    ev:      Literal['art', 'art_delete'], *,
    check:   Optional[Callable[[Art], bool]] = None,
    timeout: Optional[float]                 = None
  ) -> Art: ...
  @overload
  async def wait_for(self,
    ev:      Literal['art_edit'], *,
    check:   Optional[Callable[[Art, Art], bool]] = None,
    timeout: Optional[float]                      = None
  ) -> Tuple[Art, Art]: ...
  @overload
  async def wait_for(self,
    ev:      Literal['item', 'item_delete'], *,
    check:   Optional[Callable[[Item], bool]] = None,
    timeout: Optional[float]                 = None
  ) -> Item: ...
  @overload
  async def wait_for(self,
    ev:      Literal['arm_edit'], *,
    check:   Optional[Callable[[Item, Item], bool]] = None,
    timeout: Optional[float]                      = None
  ) -> Tuple[Item, Item]: ...
  @overload
  async def wait_for(self,
    ev:      Literal['attack', 'attack_delete'], *,
    check:   Optional[Callable[[Attack], bool]] = None,
    timeout: Optional[float]                    = None
  ) -> Attack: ...
  @overload
  async def wait_for(self,
    ev:      Literal['attack_edit'], *,
    check:   Optional[Callable[[Attack, Attack], bool]] = None,
    timeout: Optional[float]                            = None
  ) -> Tuple[Attack, Attack]: ...
  @overload
  async def wait_for(self,
    ev:      Literal['player', 'player_delete'], *,
    check:   Optional[Callable[[Player], bool]] = None,
    timeout: Optional[float]                    = None
  ) -> Player: ...
  @overload
  async def wait_for(self,
    ev:      Literal['player_edit'], *,
    check:   Optional[Callable[[Player, Player], bool]] = None,
    timeout: Optional[float]                            = None
  ) -> Tuple[Player, Player]: ...
  def wait_for(self,
    ev:      str, *,
    check:   Optional[Callable[..., bool]] = None,
    timeout: Optional[float]               = None
  ) -> Any:
    check =   check or (lambda *args: True)
    timeout = timeout or 60.0
    
    future = self.loop.create_future()

    ev = ev.lower()

    self._dispatch.add_listener(ev, future, check)

    return asyncio.wait_for(future, timeout=timeout)
  
class MorkatoWebSocketManager(MorkatoWebSocket):
  DEFAULT_GATEWAY = yarl.URL(os.getenv('GATEWAY', 'ws://localhost:5050'))
  
  @classmethod
  async def from_client(cls, client: MorkatoClientManager, login: str, *, gateway: yarl.URL = utils.UNDEFINED) -> MorkatoWebSocket:
    gateway = gateway if utils.nis_undefined(gateway) else cls.DEFAULT_GATEWAY
    
    return await super().from_client(client, login, gateway=gateway)