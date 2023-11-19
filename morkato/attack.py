from __future__ import annotations

from typing_extensions import Self
from typing import Optional, Union, List, TYPE_CHECKING, Set

if TYPE_CHECKING:
  from .utils.abc import Snowflake
  from .types import Attack as TypeAttack

  from . import (
    MorkatoClientManager,
    Guild,
    Art,
    Item
  )

from datetime import datetime
from .        import utils

import discord

__all__ = (
  'Attack',
  'ArtAttack',
  'ItemAttack',
  'ParentAttack'
)

class Attack:
  ITEMS: Set[Attack] = set()

  @staticmethod
  def get(guild: Union[Snowflake, int], id: int) -> Union[Attack, None]:
    guild_id = guild if isinstance(guild, int) else guild.id

    unique = hash((guild_id, id))

    return utils.get(Attack.ITEMS, lambda a: hash(a) == unique)
  
  @staticmethod
  def create(client: MorkatoClientManager, payload: TypeAttack) -> Attack:
    attack = Attack.get(int(payload['guild_id']), int(payload['id']))

    if not attack:
      attack = Attack(client, payload)

      Attack.ITEMS.add(attack)
    
    return attack

  def __init__(
    self,
    client:  MorkatoClientManager,
    payload: TypeAttack
  ) -> None:
    self.client = client

    self._morkato_guild:  Union[Guild, None]     = None
    self._morkato_parent: Union[ArtAttack, None] = None
    self._morkato_item:   Union[Item, None]       = None
    self._morkato_art:    Union[Art, None]       = None

    self._load_variables(payload)

  def __hash__(self) -> int:
    return hash((self._guild_id, self._id))

  def _load_variables(self, payload: TypeAttack) -> None:
    self._name      = payload['name']
    self._id        = int(payload['id'])
    self._parent_id = int(payload['parent_id']) if payload['parent_id'] else None

    self._art_id   = int(payload['art_id']) if payload['art_id'] else None
    self._item_id   = int(payload['item_id']) if payload['item_id'] else None
    self._guild_id = int(payload['guild_id'])

    self._damage = payload['damage']
    self._breath = payload['breath']
    self._blood  = payload['blood']

    self._title       = payload['embed_title']
    self._description = payload['embed_description']
    self._image_url   = payload['embed_url']
  
  def __repr__(self) -> str:
    return self._name
  
  @property
  def guild(self) -> Guild:
    if not self._morkato_guild:
      self._morkato_guild = self.client.database.get_guild(self._guild_id)
    
    if self._morkato_guild.id != self._guild_id:
      self._morkato_guild = None

      return self.guild
    
    return self._morkato_guild
  
  @property
  def parent(self) -> Union[ParentAttack, None]:
    if not self._parent_id:
      return
    
    if not self._morkato_parent:
      self._morkato_parent = None

  @property
  def art(self) -> Union[Art, None]:
    if not self._art_id:
      return
    
    if not self._morkato_art:
      if self.parent:
        return self._morkato_parent.art
      else:
        self._morkato_art = self.guild.arts.get(self._art_id)
    
    if self._morkato_art.id != self._art_id:
      self._morkato_art = None

      return self.art
    
    return self._morkato_art
  
  @property
  def item(self) -> Union[Item, None]:
    if not self._item_id:
      return
    
    if not self._morkato_item:
      self._morkato_item = self.guild.get_item(self._item_id)

    if self._morkato_item.id != self._item_id:
      self._morkato_item = None

      return self.item
    
    return self._morkato_item
  
  @property
  def parents(self) -> List[ArtAttack]:
    return sorted((atk for atk in self.guild._attacks.parent_attacks if atk.parent_id == self._id), key=lambda atk: atk.created_at.timestamp())
  
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def id(self) -> int:
    return self._id
  
  @property
  def guild_id(self) -> int:
    return self._guild_id
  
  @property
  def item_id(self) -> Union[int, None]:
    return self._item_id
  
  @property
  def art_id(self) -> Union[int, None]:
    return self._art_id
  
  @property
  def parent_id(self) -> Union[int, None]:
    return self._parent_id
  
  @property
  def required_roles(self) -> int:
    return self._required_roles

  @property
  def required_exp(self) -> int:
    return self._required_exp
  
  @property
  def damage(self) -> int:
    return self._damage
  
  @property
  def breath(self) -> int:
    return self._breath
  
  @property
  def blood(self) -> int:
    return self._blood
  
  @property
  def title(self) -> Union[str, None]:
    return self._title
  
  @property
  def description(self) -> Union[str, None]:
    return self._description
  
  @property
  def image_url(self) -> Union[str, None]:
    return self._image_url
  
  @property
  def created_at(self) -> datetime:
    return utils.created_at(self)
  
  @property
  def embed(self) -> discord.Embed:
    return self.embed_at()
  
  async def edit(self,
    name:        Optional[str] = utils.UNDEFINED,
    damage:      int           = utils.UNDEFINED,
    breath:      int           = utils.UNDEFINED,
    blood:       int           = utils.UNDEFINED,
    title:       Optional[str] = utils.UNDEFINED,
    description: Optional[str] = utils.UNDEFINED,
    url:         Optional[str] = utils.UNDEFINED
  ) -> Self:
    nis_undefined = utils.nis_undefined
    
    payload = {  }

    if nis_undefined(name):
      payload['name'] = name

    if nis_undefined(damage):
      payload['damage'] = damage
    
    if nis_undefined(breath):
      payload['breath'] = breath

    if nis_undefined(blood):
      payload['blood'] = blood

    if nis_undefined(title):
      payload['embed_title'] = title

    if nis_undefined(description):
      payload['embed_description'] = description
    
    if nis_undefined(url):
      payload['embed_url'] = url

    if not payload:
      return self

    data = await self.client.api.edit_attack(guild_id=self.guild_id, id=self.id, **payload)

    return Attack(self.client, data)

  def embed_at(self, *,
    title:       Optional[str] = utils.UNDEFINED,
    description: Optional[str] = utils.UNDEFINED,
    url:         Optional[str] = utils.UNDEFINED,
  ) -> discord.Embed:
    format  = utils.format_text
    num_fmt = utils.num_fmt
    
    title       = title or self.title
    description = description or self.description
    url         = url or self.image_url
    
    damage = num_fmt(self.damage, 2)
    breath = num_fmt(self.breath, 2)
    blood  = num_fmt(self.blood,  2)
    
    embed = discord.Embed(
      title=format(title, name=self.name) if title else title,
      description=format(description,
        name=self.name,
        damage=damage,
        breath=breath,
        blood=blood
      ) if description else 'No description'
    )

    if url:
      embed.set_image(url=url)

    embed.set_footer(text=f'ID: {self.id}')

    return embed
  
  async def delete(self) -> Attack:
    payload = await self.client.api.del_attack(
      guild_id=self.guild_id,
      id=self.id
    )

    self._load_variables(payload)

    return self
  
class ArtAttack(Attack):
  art_id: int
  art:    Art

class ParentAttack(ArtAttack):
  parent_id: int
  parent:    ArtAttack

class ItemAttack(Attack):
  arm_id: int
  item:   Item