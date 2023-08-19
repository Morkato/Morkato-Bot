from __future__ import annotations

from typing import (
  Optional,
  Generator,
  Literal,
  Iterator,
  Sequence,
  
  TYPE_CHECKING,
  List,
  Any
)

from .attack import Attack
from .art    import Art

if TYPE_CHECKING:
  from morkato.client import Morkato
  from ..types        import guild

from errors import NotFoundError

class Guild:
  def __init__(
    self, *,
    db:      Morkato,
    payload: guild.Guild
  ) -> None:
    self.db = db

    self._load_variables(payload)

  def _load_variables(self, payload: guild.Guild) -> None:
    self.__id = payload['id']

    self.__created_at = payload['created_at']
    self.__updated_at = payload['updated_at']

  def get_art_by_name(self, name: str) -> List[Art]:
    print('aqui')
    
    result = list(self.db.arts.where(guild=self, name=name))

    print(result)

    if not result:
      raise NotFoundError
    
    return result

  def get_attack_by_name(self, name: str) -> Attack:
    result = next(self.db.attacks.where(guild=self, name=name), None)

    if not result:
      raise NotFoundError
    
    return result
  
  async def create_art(self, *,
    name:              str,
    type:              Literal['RESPIRATION', 'KEKKIJUTSU'],
    embed_title:       Optional[str] = None,
    embed_description: Optional[str] = None,
    embed_url:         Optional[str] = None
  ) -> Art:
    self.db.create_attack
    return Art(
      db      = self.db,
      payload = await self.db.create_art(
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
  def __init__(self, guilds: List[Guild]) -> None:
    self.__items = guilds

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