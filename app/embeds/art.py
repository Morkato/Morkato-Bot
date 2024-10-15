from .base import BaseEmbedBuilder
from discord.embeds import Embed
from morkato.art import Art

class ArtBuilder(BaseEmbedBuilder):
  def __init__(self, art: Art) -> None:
    self.attacks = art.attacks
    self.art = art
    self.attack_line_style = self.builder.safe_get_content_unknown_formatting(self.LANGUAGE, "attackLineStyle")
    self.default_embed_description = self.builder.safe_get_content_unknown_formatting(self.LANGUAGE, "defaultEmbedDescription")
    key: str
    if art.type == art.RESPIRATION:
      key = "artRespirationTitle"
    elif art.type == art.KEKKIJUTSU:
      key = "artKekkijutsuTitle"
    elif art.type == art.FIGHTING_STYLE:
      key = "artFightingStyleTitle"
    self.title = self.builder.get_content(self.LANGUAGE, key, art=art)
  async def build_base_embed(self) -> Embed:
    description = self.art.description or self.default_embed_description
    embed = Embed(
      title=self.title,
      description=description
    )
    if self.art.banner is not None:
      embed.set_image(url=self.art.banner)
    return embed
  async def build(self, page: int) -> Embed:
    embed = await self.build_base_embed()
    description = embed.description    
    description += "\n\n"
    start_chunk = page * self.CHUNK_SIZE
    try:
      for idx in range(start_chunk, start_chunk + self.CHUNK_SIZE):
        attack = self.attacks[idx]
        prefix = attack.name_prefix_art or self.art.name
        description += self.attack_line_style.format(index=idx+1, prefix=prefix, art=self.art, attack=attack)
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
class ArtCreatedBuilder(ArtBuilder):
  def __init__(self, art: Art) -> None:
    super().__init__(art)
    self.footer_text: str
    if self.art.type == self.art.RESPIRATION:
      self.footer_text = self.builder.safe_get_content_unknown_formatting(self.LANGUAGE, "respirationCreated")
    elif self.art.type == self.art.KEKKIJUTSU:
      self.footer_text = self.builder.safe_get_content_unknown_formatting(self.LANGUAGE, "kekkijutsuCreated")
    elif self.art.type == self.art.FIGHTING_STYLE:
      self.footer_text = self.builder.safe_get_content_unknown_formatting(self.LANGUAGE, "fightingStyleCreated")
  async def build_base_embed(self):
    embed = await super().build_base_embed()
    embed.set_footer(
      icon_url = self.DEFAULT_ICON,
      text = self.footer_text.format(art=self.art)
    )
    return embed