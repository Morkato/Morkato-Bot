from __future__ import annotations

from typing_extensions import Self
from typing import (
  Optional,
  Union,
  
  List,
  Set,
  TYPE_CHECKING
)

if TYPE_CHECKING:
  from .types import Art as TypeArt, ArtType
  from .utils.abc import Snowflake

  from . import (
    MorkatoClientManager,
    ArtAttack,
    Guild
  )

from datetime import datetime
from .        import utils

import discord

__all__ = (
  'Art',
)

LIMIT_PAGE = 10

class Art:
  ITEMS: Set[Art] = set()

  @staticmethod
  def get(guild: Union[Snowflake, int], id: int) -> Union[Art, None]:
    guild_id = guild if isinstance(guild, int) else guild.id

    unique = hash((guild_id, id))

    return utils.get(Art.ITEMS, lambda a: hash(a) == unique)
  
  @staticmethod
  def create(client: MorkatoClientManager, payload: TypeArt) -> Art:
    art = Art.get(int(payload['guild_id']), int(payload['id']))

    if not art:
      art = Art(client, payload)

      Art.ITEMS.add(art)
    
    return art

  def __init__(
    self,
    client: MorkatoClientManager,
    payload: TypeArt
  ) -> None:
    self.client = client

    self._morkato_guild: Union[Guild, None] = None

    self._load_variables(payload)

  def __hash__(self) -> int:
    return hash((self._guild_id, self._id))

  def _load_variables(self, payload: TypeArt) -> None:
    self._name = payload['name']
    self._type = payload['type']
    self._id   = int(payload['id'])

    self._guild_id = int(payload['guild_id'])

    self._excluded = payload['exclude']

    self._title       = payload['embed_title']
    self._description = payload['embed_description']
    self._image_url   = payload['embed_url']
  
  def __repr__(self) -> str:
    type = 'Respiration' if self.type == 'RESPIRATION' else 'Kekkijutsu' if self.type == 'KEKKIJUTSU' else 'FightStyle'
    
    return f'<Art.{type} name={self._name!r} exclude={self._excluded}>'
  
  async def edit(self,
    name:        Optional[str]     = utils.UNDEFINED,
    type:        Optional[ArtType] = utils.UNDEFINED,
    title:       Optional[str]     = utils.UNDEFINED,
    description: Optional[str]     = utils.UNDEFINED,
    url:         Optional[str]     = utils.UNDEFINED
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
  
  def embed_at(
    self, *,
    title:       Optional[str] = utils.UNDEFINED,
    description: Optional[str] = utils.UNDEFINED,
    url:         Optional[str] = utils.UNDEFINED
  ) -> list[discord.Embed]:
    format = utils.format_text

    title = format(title or self.title or self.name, name=self.name)
    description = format(description or self.description, name=self.name, title=title) if description or self.description else 'No description'
    url = url or self.image_url

    make_embed = lambda: discord.Embed(
      title=title,
      description=description
    ).set_image(url=url).set_footer(text=f'ID: {self.id}')

    attacks = self.attacks

    if not attacks:
      return [make_embed(),]
    
    def fmt(idx: int, attack: ArtAttack) -> str:
      text = f'{idx} - !a `{attack.name}`'

      parents = attack.parents

      if not parents:
        return text
      
      return text + '\n>  ' + '\n>  '.join(f'{idx} - !a `{atk.name}`' for idx, atk in enumerate(parents, start=1))
    
    return [
      make_embed().add_field(
        name="Attacks",
        value='**%s**'%'\n'.join(
          fmt(index, attack) for index, attack in enumerate((atk for atk in attacks[i:i+LIMIT_PAGE] if not atk.parent_id), start=i+1)
        )) for i in range(0, len(attacks), 10)
      ]
  
  async def delete(self) -> Self:
    payload = await self.client.api.del_art(guild_id=self.guild_id, id=self.id)

    self._load_variables(payload)

    return self

  @property
  def guild(self) -> Guild:
    if not self._morkato_guild:
      self._morkato_guild = self.client.get_morkato_guild(self._guild_id)

    if self._morkato_guild.id != self._guild_id:
      self._morkato_guild = None

      return self.guild
    
    return self._morkato_guild
  
  @property
  def attacks(self) -> List[ArtAttack]:
    return sorted((attack for attack in self.guild._attacks.art_attacks if attack.art_id == self._id), key=lambda atk: atk._id)

  @property
  def excluded(self) -> bool:
    return self._excluded
  
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def type(self) -> ArtType:
    return self._type
  
  @property
  def guild_id(self) -> int:
    return self._guild_id
  
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
  def created_at(self) -> datetime:
    return utils.created_at(self)
