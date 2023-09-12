from __future__ import annotations

from typing_extensions import Self
from typing import (
  Iterator,
  Optional,
  Sequence,
  Literal, 
  Union,
  
  TYPE_CHECKING,
  List,
)


from .types   import Art as TypeArt, ArtType
from ..errors import NotFoundError
from ..       import utils

from copy import deepcopy

import discord

if TYPE_CHECKING:
  from ..client import MorkatoClientManager
  from .attack        import ArtAttack
  from .guild         import Guild

LIMIT_PAGE = 10

class Art:
  def __init__(
    self,
    client: MorkatoClientManager,
    payload: TypeArt
  ) -> None:
    self.client = client

    self._load_variables(payload)

  def _load_variables(self, payload: TypeArt) -> None:
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
    return self.client.database.get_guild(self.guild_id)
  
  @property
  def attacks(self) -> utils.GenericGen[ArtAttack]:
    return self.client.database.attacks.where(guild_id=self.guild_id, art=self)

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
    name:              Optional[str]     = utils.UNDEFINED,
    type:              Optional[ArtType] = utils.UNDEFINED,
    title:             Optional[str]     = utils.UNDEFINED,
    description:       Optional[str]     = utils.UNDEFINED,
    url:               Optional[str]     = utils.UNDEFINED
  ) -> Self:
    nis_undefined = utils.nis_undefined

    if (
      nis_undefined(name)
      and nis_undefined(type)
      and nis_undefined(title)
      and nis_undefined(description)
      and nis_undefined(url)
    ):
      return self
    
    data = await self.client.api.edit_art(self.guild_id, self.id,
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
    title:       Optional[str] = utils.UNDEFINED,
    description: Optional[str] = utils.UNDEFINED,
    url:         Optional[str] = utils.UNDEFINED
  ) -> list[discord.Embed]:
    format = utils.format_text

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
  
  async def delete(self) -> Self:
    payload = await self.client.api.del_art(guild_id=self.guild_id, id=self.id)

    self._load_variables(payload)

    return self

class Arts(Sequence[Art]):
  def __init__(self, *arts: List[Art]) -> None:
    self.__items = list(arts)

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

  def add(self, *arts: Art) -> None:
    if not all(isinstance(art, Art) for art in arts):
      raise TypeError

    self.__items.extend(arts)

  def delete(self, guild_id: str, id: str) -> Art:
    index, art = next(((i, item) for i, item in enumerate(self) if item.guild_id == guild_id and id == item.id), (-1, None))

    if index == -1 or not art:
      raise NotFoundError
    
    del self[index]

    return art

  def where(self, *,
      name:     str     = utils.UNDEFINED,
      id:       str     = utils.UNDEFINED,
      type:     ArtType = utils.UNDEFINED,
      guild:    Guild   = utils.UNDEFINED,
      guild_id: str     = utils.UNDEFINED
    ) -> utils.GenericGen[Art]:
    nis_undefined = utils.nis_undefined

    if nis_undefined(guild):
      guild_id = guild.id

    if nis_undefined(name):
      name = utils.strip_text(name,
        ignore_accents=True,
        ignore_empty=True,
        case_insensitive=True,
        strip_text=True
      )

    def checker(art: Art) -> bool:
      if nis_undefined(id) and not art.id == id:
        return False
      
      if nis_undefined(guild_id) and not art.guild_id == guild_id:
        return False
      
      if nis_undefined(name) and not name == utils.strip_text(art.name,
        ignore_accents=True,
        ignore_empty=True,
        case_insensitive=True,
        strip_text=True
      ):
        return False
      
      if nis_undefined(type) and not art.type == type:
        return False
      
      return True
    
    return (item for item in self if checker(item))
  
  def __delitem__(self, k: int) -> None:
    del self.__items[k]