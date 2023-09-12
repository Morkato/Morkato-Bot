from __future__ import annotations

from typing import (
  Optional,
  Iterator,
  Sequence,
  Union,
  
  TYPE_CHECKING,
  List,
)

from .player import Player, PlayerBreed
from .art    import ArtType, Arts, Art
from .attack import Attacks, Attack

if TYPE_CHECKING:
  from ..client import MorkatoClientManager

  from .types        import guild

from .. import (
  errors,
  utils
)

import discord

class Guild:
  def __init__(
    self, *,
    client:  MorkatoClientManager,
    payload: guild.Guild
  ) -> None:
    self.client = client

    self._load_variables(payload)

  @property
  def discord(self) -> Union[discord.Guild, None]:
    return self.client.get_guild(int(self.id))

  def _load_variables(self, payload: guild.Guild) -> None:
    self.__id = payload['id']

    self.__created_at = payload['created_at']
    self.__updated_at = payload['updated_at']

  def get_player(self, id: str) -> Player:
    return self.client.database.get_player(guild_id=self.id, id=id)
  
  def get_arts_by_name(self, name: str) -> List[Art]:
    result = list(self.client.database.arts.where(guild=self, name=name))

    if not result:
      raise errors.NotFoundError('Essa arte não existe.')
    
    return result

  def get_attacks_by_name(self, name: str) -> List[Attack]:
    result = list(self.client.database.attacks.where(guild=self, name=name))

    if not result:
      raise errors.NotFoundError('Esse ataque não existe.')
    
    return result
  
  async def create_art(self, *,
    name:              str,
    type:              ArtType,
    embed_title:       Optional[str] = utils.UNDEFINED,
    embed_description: Optional[str] = utils.UNDEFINED,
    embed_url:         Optional[str] = utils.UNDEFINED
  ) -> Art:
    return Art(
      client  = self.client,
      payload = await self.client.api.create_art(
        guild_id=self.id,
        name=name,
        type=type,
        embed_title=embed_title,
        embed_description=embed_description,
        embed_url=embed_url
      )
    )
  
  async def create_attack(self, *, 
    name:              str,
    parent:            Optional[Attack]       = utils.UNDEFINED,
    art:               Optional[Art]          = utils.UNDEFINED,
    embed_title:       Optional[str]          = utils.UNDEFINED,
    embed_description: Optional[str]          = utils.UNDEFINED,
    embed_url:         Optional[str]          = utils.UNDEFINED
  ) -> Attack:
    parent_id = parent if not parent else parent.id
    art_id    = art if not art else art.id
    
    payload = await self.client.api.create_attack(
      guild_id=self.id,
      name=name,
      parent=parent_id,
      art_id=art_id,
      embed_title=embed_title,
      embed_description=embed_description,
      embed_url=embed_url
    )

    return Attack(client=self.client, payload=payload)
  
  async def create_player(self, *,
    id:          str,
    name:        str,
    breed:       PlayerBreed,
    credibility: Optional[int] = utils.UNDEFINED,
    cash:        Optional[int] = utils.UNDEFINED,
    life:        Optional[int] = utils.UNDEFINED,
    breath:      Optional[int] = utils.UNDEFINED,
    blood:       Optional[int] = utils.UNDEFINED,
    exp:         Optional[int] = utils.UNDEFINED,
    appearance:  Optional[str] = utils.UNDEFINED
  ) -> Player:
    payload = await self.client.api.create_player(
      guild_id=self.id,
      id=id,
      name=name,
      breed=breed,
      credibility=credibility,
      cash=cash,
      life=life,
      breath=breath,
      blood=blood,
      exp=exp,
      appearance=appearance
    )

    return Player(client=self.client, payload=payload)
  
  @property
  def id(self) -> str:
    return self.__id
  
  @property
  def created_at(self) -> str:
    return self.__created_at
  
  @property
  def updated_at(self) -> str:
    return self.__updated_at
  
  @property
  def arts(self) -> Arts:
    return Arts(*self.client.database.arts.where(guild=self))
  
  @property
  def attacks(self) -> Attacks:
    return Attacks(*self.client.database.attacks.where(guild=self))

class Guilds(Sequence[Guild]):
  def __init__(self, *guilds: List[Guild]) -> None:
    self.__items = list(guilds)

  def __iter__(self) -> Iterator[Guild]:
    return iter(self.__items)
  
  def __getitem__(self, k: str) -> Guild:
    return self.get(k)
  
  def __len__(self) -> int:
    return len(self.__items)
  
  def get(self, id: str) -> Guild:
    guild = next(self.where(id=id), None)

    if not guild:
      raise errors.NotFoundError('Seu servidor não está registrado em meu banco de dados, registre ele.')
    
    return guild

  def add(self, *guilds: Guild) -> None:
    if not all(isinstance(guild, Guild) for guild in guilds):
      raise TypeError

    self.__items.extend(guilds)

  def where(self, *, id: Optional[str] = utils.UNDEFINED) -> utils.GenericGen[Guild]:
    def checker(guild: Guild) -> bool:
      if utils.nis_undefined(id) and not guild.id == id:
        return False
      
      return True
    
    return (item for item in self if checker(item))
  
  def __delitem__(self, k: int) -> None:
    del self.__items[k]