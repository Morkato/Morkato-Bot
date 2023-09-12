from __future__ import annotations

from typing_extensions import Self
from typing import (
  Generator,
  Iterator,
  Iterable,
  Optional,
  Sequence,
  Union,
  
  overload,
  
  List,
  TYPE_CHECKING,
  Any
)

from morkato.objects.types import Attack as TypeAttack

if TYPE_CHECKING:
  from morkato.client import MorkatoClientManager

  from .types import Attack as TypeAttack
  from .guild import Guild
  from .art   import Art

from ..errors import NotFoundError
from ..       import utils

import discord

class Attack:
  def __init__(
    self,
    client:  MorkatoClientManager,
    payload: TypeAttack
  ) -> None:
    self.client = client

    self._load_variables(payload)

  def _load_variables(self, payload: TypeAttack) -> None:
    self.__name   = payload['name']
    self.__id     = payload['id']
    self.__parent = payload['parent_id']

    self.__art_id = payload['art_id']
    self.__guild_id = payload['guild_id']

    self.__title       = payload['embed_title']
    self.__description = payload['embed_description']
    self.__image_url   = payload['embed_url']
  
  def __repr__(self) -> str:
    return self.__name
  
  def __eq__(self, other) -> bool:
    if isinstance(other, Attack):
      return self.guild.id == other.guild.id and self.__name == other.name
    
    return False
  
  @property
  def name(self) -> str:
    return self.__name
  
  @property
  def id(self) -> str:
    return self.__id
  
  @property
  def guild_id(self) -> str:
    return self.__guild_id
  
  @property
  def guild(self) -> Guild:
    return self.client.database.get_guild(self.guild_id)
  
  @property
  def parent_id(self) -> str:
    return self.__parent
  
  @property
  def parent(self) -> Attack:
    return self.client.database.get_attack(guild_id=self.guild_id, id=self.parent_id)
  
  @property
  def parents(self) -> Generator[Attack]:
    return self.client.database.attacks.where(guild=self.guild, parent=self.id)
  
  @property
  def art_id(self) -> Union[str, None]:
    return self.__art_id
  
  @property
  def art(self) -> Union[Art, None]:
    if not self.art_id:
      return
    
    return self.client.database.get_art(guild_id=self.guild_id, id=self.art_id)
  
  @property
  def required_roles(self) -> int:
    return self.__required_roles

  @property
  def required_exp(self) -> int:
    return self.__required_exp
  
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
    name:           Optional[str] = None,
    title:          Optional[str] = None,
    description:    Optional[str] = None,
    url:            Optional[str] = None
  ) -> Self:
    payload = {  }

    if name:
      payload['name'] = name

    if title:
      payload['embed_title'] = title

    if description:
      payload['embed_description'] = description
    
    if url:
      payload['embed_url'] = url

    if not payload:
      return self

    data = await self.client.api.edit_attack(guild_id=self.guild_id, id=self.id, **payload)

    self._load_variables(data)

    return self

  async def embed_at(self,
    member:      Optional[discord.Member] = None, *,
    title:       Optional[str]            = None,
    description: Optional[str]            = None,
    url:         Optional[str]            = None,
  ) -> discord.Embed:
    title       = title or self.title or self.name
    description = description or self.description
    url         = url or self.image_url

    embed = discord.Embed(
      title=format(title, name=self.name),
      description=format(description, name = self.name) if description else 'No description'
    )

    if url:
      embed.set_image(url=url)

    parents = list(self.parents)

    if parents:
      embed.add_field(name='Parent Attacks', value='\n'.join(f'!a **`{parent.name}`**' for parent in parents))

    embed.set_footer(text=f'ID: {self.id}')

    return embed
  
  async def delete(self) -> Attack:
    payload = await self.db.del_attack(
      guild_id=self.guild_id,
      id=self.id
    )

    self._load_variables(payload)

    return self
  
class ArtAttack(Attack):
  def _load_variables(self, payload: Attack) -> None:
    result = super()._load_variables(payload)

    if self.__art_id is None:
      raise TypeError('Attack Art required art!')
    
    return result
  
  @property
  def art(self) -> Art:
    return super().art
  
class Attacks(Sequence[Attack]):
  def __init__(self, *attacks: List[Attack]) -> None:
    self.__items = list(attacks)

  def __iter__(self) -> Iterator[Attack]:
    return iter(self.__items)
  
  def __len__(self) -> int:
    return len(self.__items)
  
  def __getitem__(self, k: int) -> Attack:
    return self.__items[k]
  
  def get(self, guild_id: str, id: str) -> Attack:
    attack = next(self.where(guild_id=guild_id, id=id), None)

    if not attack:
      raise NotFoundError
    
    return attack

  def add(self, *attacks: Attack) -> None:
    if not all(isinstance(item, Attack) for item in attacks):
      raise TypeError
    
    self.__items.extend(attacks)
  
  def delete(self, guild_id: str, id: str) -> Art:
    index, attack = next(((i, item) for i, item in enumerate(self) if item.guild_id == guild_id and id == item.id), (-1, None))

    if index == -1 or not attack:
      raise NotFoundError('Esse ataque não existe.')
    
    del self[index]

    return attack

  @overload
  def where(
    self, *,
    guild:     Guild  = utils.UNDEFINED,
    guild_id:  str    = utils.UNDEFINED,
    name:      str    = utils.UNDEFINED,
    id:        str    = utils.UNDEFINED,
    parent:    Attack = utils.UNDEFINED,
    parent_id: str    = utils.UNDEFINED
  ) -> utils.GenericGen[Attack]: ...
  @overload
  def where(
    self, *,
    art:       Art,
    guild:     Guild  = utils.UNDEFINED,
    guild_id:  str    = utils.UNDEFINED,
    name:      str    = utils.UNDEFINED,
    id:        str    = utils.UNDEFINED,
    parent:    Attack = utils.UNDEFINED,
    parent_id: str    = utils.UNDEFINED
  ) -> utils.GenericGen[ArtAttack]: ...
  @overload
  def where(
    self, *,
    art_id: str,
    guild:    Guild  = utils.UNDEFINED,
    guild_id: str    = utils.UNDEFINED,
    name:     str    = utils.UNDEFINED,
    id:       str    = utils.UNDEFINED,
    parent:   Attack = utils.UNDEFINED,
    parent_id: str   = utils.UNDEFINED
  ) -> utils.GenericGen[ArtAttack]: ...
  def where(
    self, *,
    art:      Art    = utils.UNDEFINED,
    art_id: str      = utils.UNDEFINED,
    guild:    Guild  = utils.UNDEFINED,
    guild_id: str    = utils.UNDEFINED,
    name:     str    = utils.UNDEFINED,
    id:       str    = utils.UNDEFINED,
    parent:   Attack = utils.UNDEFINED,
    parent_id: str   = utils.UNDEFINED
  ) -> Generator[Attack]:
    nis_undefined = utils.nis_undefined
    
    if nis_undefined(guild):
      guild_id = guild.id

    if nis_undefined(art):
      art_id = art.id

    if nis_undefined(parent):
      parent_id = parent.id

    if nis_undefined(name):
      name = utils.strip_text(name,
        ignore_accents=True,
        ignore_empty=True,
        case_insensitive=True,
        strip_text=True      
      )
    
    def checker(attack: Attack) -> bool:
      if nis_undefined(id) and not attack.id == id:
        return False
      
      if nis_undefined(guild_id) and not guild_id == attack.guild_id:
        return False
      
      if nis_undefined(art_id) and not art_id == attack.art_id:
        return False
      
      if nis_undefined(name) and not name == utils.strip_text(attack.name,
        ignore_accents=True,
        ignore_empty=True,
        case_insensitive=True,
        strip_text=True      
      ):
        return False
      
      if nis_undefined(parent_id) and not parent_id == attack.parent_id:
        return False
      
      return True
    
    return (item for item in self if checker(item))
  
  def __delitem__(self, k: int) -> None:
    del self.__items[k]