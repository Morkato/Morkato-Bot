from __future__ import annotations

from typing import (
  Iterator,
  Optional,
  Generator,
  Sequence,
  Literal, 
  Union,
  
  TYPE_CHECKING,
  List,
  Any
)

from utils.etc import format, toKey

from .attack import ArtAttack
from ..types import art

from errors import NotFoundError

from copy import deepcopy

import discord

if TYPE_CHECKING:
  from morkato.client import Morkato
  from .guild         import Guild

LIMIT_PAGE = 10

class Art:
  def __init__(
    self,
    db:      Morkato,
    payload: art.Art
  ) -> None:
    self.db  = db

    self._load_variables(payload)

  def _load_variables(self, payload: art.Art) -> None:
    self.__name = payload['name']
    self.__type = payload['type']
    self.__id   = payload['id']

    self.__guild_id = payload['guild_id']

    self.__title       = payload['embed_title']
    self.__description = payload['embed_description']
    self.__image_url   = payload['embed_url']

  def __repr__(self) -> str:
    return self.__name

  def __eq__(self, other) -> bool:
    if isinstance(other, Art):
      return self.guild.id == other.guild.id and self.__name == other.name
    
    return False
  
  @property
  def name(self) -> str:
    return self.__name
  
  @property
  def id(self) -> str:
    return self.__id
  
  @property
  def guild(self) -> Guild:
    return self.db.guilds.get(self.guild_id)
  
  @property
  def attacks(self) -> Generator[Any, Any, ArtAttack]:
    return self.db.attacks.where(guild_id=self.guild_id, art=self)

  @property
  def type(self) -> Literal['RESPIRATION', 'KEKKIJUTSU']:
    return self.__type
  
  @property
  def guild_id(self) -> str:
    return self.__guild_id
  
  @property
  def title(self) -> Union[str, None]:
    return self.__title
  
  @property
  def description(self) -> Union[str, None]:
    return self.__description
  
  @property
  def image_url(self) -> Union[str, None]:
    return self.__image_url
  
  async def edit(self,
    name:              Optional[str]          = None,
    type:              Optional[art.ArtType]  = None,
    title:             Optional[str]          = None,
    description:       Optional[str]          = None,
    url:               Optional[str]          = None
  ) -> Art:
    if (
      not name
      and not type
      and not title
      and not description
      and not url
    ):
      return self
    
    data = await self.db.edit_art(self.guild_id, self.id,
      name=name,
      type=type,
      embed_title=title,
      embed_description=description,
      embed_url=url
    )

    self._load_variables(data)

    return self
  
  async def embed_at(
    self, *,
    title: Optional[str] = None,
    description: Optional[str] = None,
    url: Optional[str] = None
  ) -> list[discord.Embed]:
    title = title or self.title or self.name
    description = format(description or self.description, title=title) if description or self.description else 'No description'
    url = url or self.image_url

    embed = discord.Embed(
      title=format(title, name=self.name),
      description=description
    )

    if url:
      embed.set_image(url=url)

    attacks = list(self.attacks)

    if not attacks:
      return [embed,]
    
    embeds = [
      deepcopy(embed).add_field(
        name="Attacks",
        value='**%s**'%'\n'.join(
          f'{index} - !a `{attack}`' for index, attack in enumerate(attacks[i:i+LIMIT_PAGE], start=i+1)
        )) for i in range(0, len(attacks), 10)
      ]

    return embeds
  
  async def delete(self) -> Art:
    await self.db.del_art(guild_id=self.guild_id, id=self.id)

    return self

class Arts(Sequence[Art]):
  def __init__(self, arts: List[Art] = None) -> None:
    self.__items = arts or []

  def __iter__(self) -> Iterator[Art]:
    return iter(self.__items)

  def __getitem__(self, k: int) -> Guild:
    return self.__items[k]
  
  def __len__(self) -> int:
    return len(self.__items)
  
  def get(self, guild_id: str, id: str) -> Art:
    art = next(self.where(guild_id=guild_id, id=id), None)

    if not art:
      raise NotFoundError('Essa arte não existe.')
    
    return art

  def add(self, art: Art) -> None:
    if not isinstance(art, Art):
      raise TypeError

    self.__items.append(art)

  def delete(self, guild_id: str, name: str) -> Art:
    index, art = next(((i, item) for i, item in enumerate(self) if item.guild_id == guild_id and toKey(name) == toKey(item.name)), (-1, None))

    if index == -1 or not art:
      raise NotFoundError
    
    del self[index]

    return art

  def where(self, *, name: Optional[str] = None, id: Optional[str] = None, type: Optional[art.ArtType] = None, guild: Optional[Guild] = None, guild_id: Optional[str] = None) -> Generator[Any, Any, Art]:
    if guild:
      guild_id = guild.id

    def checker(art: Art) -> bool:
      if id and not art.id == id:
        return False
      
      if guild_id and not art.guild_id == guild_id:
        return False
      
      if name and not toKey(name) == toKey(art.name):
        return False
      
      if type and not art.type == type:
        return False
      
      return True
    
    return (item for item in self if checker(item))
  
  def __delitem__(self, k: int) -> None:
    del self.__items[k]