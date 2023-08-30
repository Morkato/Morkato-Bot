from __future__ import annotations

from typing_extensions import Self
from typing import (
  Optional,
  Generator,
  
  List,

  TYPE_CHECKING
)

if TYPE_CHECKING:
  from .gateway import MorkatoWebSocketManager
  from .client  import MorkatoClientManager

from objects.types import (
  Player as TypedPlayer,
  Attack as TypedAttack,
  Guild  as TypedGuild,
  Art    as TypedArt
)

from objects import (
  Players,
  Attacks,
  Guilds,
  Arts,

  Player,
  Attack,
  Guild,
  Art
)

class MorkatoDatabaseManager:
  def __init__(
    self,
    client: MorkatoClientManager, *,
    guilds: Optional[List[TypedGuild]]   = None,
    attacks: Optional[List[TypedAttack]] = None,
    players: Optional[List[TypedPlayer]] = None,
    arts: Optional[List[TypedArt]]       = None
  ) -> None:
    self.__client = client

    guilds  = guilds  or []
    attacks = attacks or []
    players = players or []
    arts    = arts    or []

    self.__guilds  = Guilds(*(Guild(client=client, payload=data) for data in guilds))
    self.__attacks = Attacks(*(Attack(client=client, payload=data) for data in attacks))
    self.__players = Players(*(Player(client=client, payload=data) for data in players))
    self.__arts    = Arts(*(Art(client=client, payload=data) for data in arts))
  
  @classmethod
  async def from_gateway(cls, client: MorkatoClientManager, gateway: MorkatoWebSocketManager) -> Self:
    (event, hello) = await gateway.pool_event()

    print(event, hello)
    
    (event, guilds)  = await gateway.pool_event()
    (event, arts)    = await gateway.pool_event()
    (event, attacks) = await gateway.pool_event()
    (event, players) = await gateway.pool_event()
    
    return cls(
      client,
      guilds=guilds,
      players=players,
      attacks=attacks,
      arts=arts
    )

  @property
  def guilds(self) -> Guilds:
    return self.__guilds
  
  @property
  def attacks(self) -> Attacks:
    return self.__attacks
  
  @property
  def players(self) -> Players:
    return self.__players
  
  @property
  def arts(self) -> Arts:
    return self.__arts

  def get_guild(self, id: str) -> Guild:
    return self.guilds.get(id)

  def get_art(self, guild_id: str, id: str) -> Art:
    return self.arts.get(guild_id, id)
  
  def get_art_by_name(self, guild_id: str, name: str) -> Generator[Art]:
    return self.arts.where(guild_id=guild_id, name=name)
  
  def get_attack(self, guild_id: str, id: str) -> Attack:
    return self.attacks.get(guild_id, id)

  def get_attack_by_name(self, guild_id: str, name: str) -> Generator[Attack]:
    return self.attacks.where(guild_id=guild_id, name=name)
  
  def get_player(self, guild_id: str, id: str) -> Player:
    return self.players.get(guild_id=guild_id, id=id)
