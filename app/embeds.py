from morkato.ext.embeds import EmbedBuilder
from morkato.attack import Attack
from discord.embeds import Embed
from morkato.types import ArtType
from morkato.art import Art
from typing import (
  ClassVar,
  Dict
)

class ArtBuilder(EmbedBuilder):
  ATTACK_LINE_STYLE: ClassVar[str] = "**{index}° - {prefix}:** {attack.name}"
  DEFAULT_EMBED_DESCRIPTION: ClassVar[str] = "No description"
  ART_TYPE_MAP: ClassVar[Dict[ArtType, str]] = {
    Art.RESPIRATION: "Respiração",
    Art.KEKKIJUTSU: "Kekkijutsu",
    Art.FIGHTING_STYLE: "Estilo de Luta"
  }
  CHUNK_SIZE: ClassVar[int] = 10
  def __init__(self, art: Art) -> None:
    self.attacks = art.attacks
    self.art = art
  async def build_base_embed(self) -> Embed:
    title = "%s: %s" % (self.ART_TYPE_MAP[self.art.type], self.art.name)
    description = self.art.description
    embed = Embed(
      title=title,
      description=description
    )
    if self.art.banner is not None:
      embed.set_image(url=self.art.banner)
    return embed
  async def build(self, page: int) -> Embed:
    embed = await self.build_base_embed()
    description = embed.description
    if description is None:
      description = self.DEFAULT_EMBED_DESCRIPTION
    description += "\n\n"
    start_chunk = page * self.CHUNK_SIZE
    try:
      for idx in range(start_chunk, start_chunk + self.CHUNK_SIZE):
        attack = self.attacks[idx]
        prefix = attack.name_prefix_art or self.art.name
        style = self.ATTACK_LINE_STYLE
        description += style.format(index=idx+1, prefix=prefix, art=self.art, attack=attack)
        description += '\n'
    except IndexError:
      pass
    embed.description = description
    return embed
  def length(self) -> int:
    length = len(self.attacks)
    if length == 0:
      return 1
    elif length % self.CHUNK_SIZE != 0:
      return length // self.CHUNK_SIZE + 1
    return length // self.CHUNK_SIZE
class AttackBuilder(EmbedBuilder):
  DEFAULT_EMBED_DESCRIPTION: ClassVar[str] = "No description"
  def __init__(self, attack: Attack) -> None:
    self.attack = attack
    self.art = attack.art
  async def build(self, page: int) -> Embed:
    title = self.attack.name_prefix_art
    if title is None:
      title = self.art.name
    title = "%s: %s" % (title, self.attack.name)
    description = self.attack.description
    if description is None:
      description = self.DEFAULT_EMBED_DESCRIPTION
    embed = Embed(
      title=title,
      description=description
    )
    if self.attack.banner is not None:
      embed.set_image(url=self.attack.banner)
    return embed
  def length(self) -> int:
    return 1