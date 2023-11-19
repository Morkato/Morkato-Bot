from __future__ import annotations

from typing_extensions import Self
from typing import (
  Union,

  List,
  TYPE_CHECKING
)

if TYPE_CHECKING:
  from .utils.abc import Snowflake

  from .types import (
    Item as TypeItem
  )

  from . import (
    MorkatoClientManager,
    ItemAttack,
    Guild
  )

from datetime import datetime
from .errors import NotFoundError
from .       import utils

import discord

LIMIT_PAGE = 10

class Item:
  ITEMS: List[Item] = []

  @staticmethod
  def get(guild: Union[Snowflake, int], id: int) -> Union[Item, None]:
    guild_id = guild if isinstance(guild, int) else guild.id

    unique = hash((guild_id, id))

    return utils.get(Item.ITEMS, lambda i: hash(i) == unique)
  
  @staticmethod
  def create(client: MorkatoClientManager, payload: TypeItem) -> Item:
    item = Item.get(int(payload['guild_id']), int(payload['id']))

    if not item:
      item = Item(client, payload)

      Item.ITEMS.append(item)

    return item

  def __init__(
    self,
    client:  MorkatoClientManager,
    payload: TypeItem
  ) -> None:
    self.client = client
    
    self._morkato_guild: Union[Guild, None]        = None # Cache for Guild MorkatoBOT
    self._morkato_role:  Union[discord.Role, None] = None # Cache for Discord Role

    self._load_variables(payload)
  
  def __repr__(self) -> str:
    return f'<Item name={self._name!r} stack={self._stack} usable={self._usable} attacks={self.attacks}>'
  
  def __hash__(self) -> int:
    return hash((self._guild_id, self._id))

  def _load_variables(self, payload: TypeItem) -> None:
    self._name = payload['name']
    self._description = payload['description']

    self._guild_id = int(payload['guild_id'])
    self._id       = int(payload['id'])

    self._usable = payload['usable']
    self._stack  = payload['stack']
    
    self._title       = payload['embed_title']
    self._description = payload['embed_description']
    self._image_url   = payload['embed_url']

    self._updated_at = datetime.fromtimestamp(payload['updated_at'] / 1000)

  @property
  def guild(self) -> Guild:
    if not self._morkato_guild:
      self._morkato_guild = self.client.get_morkato_guild(self._guild_id)

    if self._morkato_guild.id != self._guild_id: # Sync Cache
      self._morkato_guild = None

      return self.guild
    
    return self._morkato_guild
  
  def get_attack(self, name: str) -> ItemAttack:
    fmt = lambda text: utils.strip_text(text,
      strip_text=True,
      ignore_empty=True,
      ignore_accents=True,
      case_insensitive=True
    )

    name = fmt(name)

    attacks = (attack for attack in self.guild._attacks.item_attacks if attack._item_id == self.id)

    result = utils.get(attacks, lambda attack: fmt(attack.name) == name)

    if not result:
      raise NotFoundError(f'Esse ataque não existe no item: **`{self._name}`**.')

    return result

  @property
  def attacks(self) -> List[ItemAttack]:
    return sorted((attack for attack in self.guild._attacks.item_attacks if attack.item_id == self.id), key=lambda attack: attack._id)

  @property
  def created_at(self) -> datetime:
    return utils.created_at(self)
  
  @property
  def updated_at(self) -> datetime:
    return self._updated_at
  
  @property
  def guild_id(self) -> int:
    return self._guild_id
  
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def description(self) -> Union[str, None]:
    return self._description
  
  @property
  def id(self) -> int:
    return self._id
  
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
  def embed(self) -> discord.Embed:
    return self.embed_at()
  
  async def edit(
    self,
    name:        str          = utils.UNDEFINED,
    stack:       int          = utils.UNDEFINED,
    usable:      bool         = utils.UNDEFINED,
    title:       str          = utils.UNDEFINED,
    description: str          = utils.UNDEFINED,
    url:         str          = utils.UNDEFINED
  ) -> Self:
    nis_undefined = utils.nis_undefined

    payload = {  }

    if nis_undefined(name):
      payload['name'] = name

    if nis_undefined(stack):
      payload['stack'] = stack
    
    if nis_undefined(usable):
      payload['usable'] = usable
    
    if nis_undefined(title):
      payload['embed_title'] = title

    if nis_undefined(description):
      payload['embed_description'] = description

    if nis_undefined(url):
      payload['embed_url'] = url

    if not payload:
      return self
    
    data = await self.client.api.edit_item(guild_id=self.guild_id, id=self.id, **payload)

    self._load_variables(data)

    return self
  
  def embed_at(
    self, *,
    title:       str = utils.UNDEFINED,
    description: str = utils.UNDEFINED,
    url:         str = utils.UNDEFINED
  ) -> List[discord.Embed]:
    title       = utils.case_undefined(title, self.title)
    description = utils.case_undefined(description, self.description)
    url         = utils.case_undefined(url, self.image_url)

    make_embed = lambda: discord.Embed(
      title = self.name if not title else utils.format_text(title, name=self.name),
      description='No description' if not description else utils.format_text(description, name=self.name)
    ).set_image(url=url).set_footer(text=f'ID: {self.id}')

    attacks = self.attacks

    if not attacks:
      return [make_embed(),]
    
    return [
      make_embed().add_field(name='Attacks', value='\n'.join((f'**{index} - !a `{self.name}: {attack.name}`**' for index, attack in enumerate(attacks[i:i+LIMIT_PAGE], start=i+1))))
      for i in range(0, len(attacks), LIMIT_PAGE)
    ]