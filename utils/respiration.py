from __future__ import annotations

from discord import Embed, Role

from .types.respiration import Respiration as TypedRespiration
from typing import Optional, TYPE_CHECKING

from .string import format

if TYPE_CHECKING:
  from .guild import Guild

class Respiration:
  def __init__(self, guild: Guild, payload: TypedRespiration) -> None:
    self.guild = guild

    self._load_variables(payload)
  def _load_variables(self, data: TypedRespiration) -> None:
    self.name = data['name']
    self.role_id = data['role']

    self.embed_title = data['embed_title']
    self.embed_desprition = data['embed_description']
    self.embed_url = data['embed_url']
  def __repr__(self) -> str:
    return f'Respiration(guild={self.guild} name={self.name})'
  
  @property
  def embed(self) -> Embed:
    return self.embed_at()
  
  def embed_at(
    self, *,
    title: Optional[str] = None,
    description: Optional[str] = None,
    url: Optional[str] = None
  ) -> Embed:
    title = title or self.embed_title or self.name
    description = format(description or self.embed_desprition, title=title) if description or self.embed_desprition else 'No description'
    url = self.embed_url

    embed = Embed(
      title=title,
      description=description
    )

    if url:
      embed.set_image(url=url)
    
    return embed
  def edit(
    self, *,
    
    name: Optional[str] = None,
    role: Optional[Role] = None,

    embed_title: Optional[str] = None,
    embed_description: Optional[str] = None,
    embed_url: Optional[str] = None
  ) -> Respiration:
    payload = {
      "name": name or self.name,
      "role": role or self.role_id,
      "embed_title": embed_title or self.embed_title,
      "embed_description": embed_description or self.embed_desprition,
      "embed_url": embed_url or self.embed_url
    }

    def check(res) -> TypedRespiration:
      if not res.status_code == 200:
        res.raise_for_status()
      
      return res.json()
    
    data = self.guild.request_element('POST', f'/respirations/{self.name}', call=check, json=payload)

    self._load_variables(data)

    return self