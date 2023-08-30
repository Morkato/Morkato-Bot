from __future__ import annotations

from typing import (
  Optional,
  Generator,
  Literal,
  Iterator,
  Sequence,
  Union,
  
  TYPE_CHECKING,
  List,
  Any
)

from .player import Player, PlayerBreed
from .attack import Attack
from .art    import Art

if TYPE_CHECKING:
  from morkato.client import MorkatoClientManager

  from ..types        import guild

from errors import NotFoundError

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
  
  def get_art_by_name(self, name: str) -> List[Art]:
    result = list(self.client.database.get_art_by_name(guild_id=self.id, name=name))

    if not result:
      raise NotFoundError('Essa arte não existe.')
    
    return result

  def get_attack_by_name(self, name: str) -> Attack:
    result = next(self.client.database.get_attack_by_name(guild_id=self.id, name=name), None)

    if not result:
      raise NotFoundError('Esse ataque não existe.')
    
    return result
  
  async def create_art(self, *,
    name:              str,
    type:              Literal['RESPIRATION', 'KEKKIJUTSU'],
    embed_title:       Optional[str] = None,
    embed_description: Optional[str] = None,
    embed_url:         Optional[str] = None
  ) -> Art:
    return Art(
      db      = self.db,
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
    parent:            Optional[Attack]       = None,
    art:               Optional[Art]          = None,
    embed_title:       Optional[str]          = None,
    embed_description: Optional[str]          = None,
    embed_url:         Optional[str]          = None
  ) -> Attack:
    parent_id = parent if not parent else parent.id
    art_id    = art if not art else art.id
    
    payload = await self.db.create_attack(
      guild_id=self.id,
      name=name,
      parent=parent_id,
      art_id=art_id,
      embed_title=embed_title,
      embed_description=embed_description,
      embed_url=embed_url
    )

    return Attack(db=self.db, payload=payload)
  
  async def create_player(self, *,
    id:          str,
    name:        str,
    breed:       PlayerBreed,
    credibility: Optional[int] = None,
    cash:        Optional[int] = None,
    life:        Optional[int] = None,
    breath:      Optional[int] = None,
    blood:       Optional[int] = None,
    exp:         Optional[int] = None,
    appearance:  Optional[str] = None
  ) -> Player:
    payload = await self.db.create_player(
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

    return Player(db=self.db, payload=payload)
  
  @property
  def id(self) -> str:
    return self.__id
  
  @property
  def created_at(self) -> str:
    return self.__created_at
  
  @property
  def updated_at(self) -> str:
    return self.__updated_at
  
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
      raise NotFoundError('Seu servidor não está registrado em meu banco de dados, registre ele.')
    
    return guild

  def add(self, guild: Guild) -> None:
    if not isinstance(guild, Guild):
      raise TypeError

    self.__items.append(guild)

  def where(self, *, id: Optional[str] = None) -> Generator[Any, Any, Guild]:
    def checker(guild: Guild) -> bool:
      if id and not guild.id == id:
        return False
      
      return True
    
    return (item for item in self if checker(item))
  
  def __delitem__(self, k: int) -> None:
    del self.__items[k]