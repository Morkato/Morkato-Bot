from __future__ import annotations

from discord.embeds import Embed

from .types.respiration import Respiration as TypedRespiration
from typing import Optional, TYPE_CHECKING

from .string import format

if TYPE_CHECKING:
  from .guild import Guild

class Respiration:
  def __init__(self, guild: Guild, payload: TypedRespiration) -> None:
    print(payload)
    
    self.name = payload['name']
    self.role_id = payload['role']

    self.embed_title = payload['embed_title']
    self.embed_desprition = payload['embed_description']
    self.embed_url = payload['embed_url']

    self.guild = guild
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
