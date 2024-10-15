from morkato.attack import Attack
from discord.embeds import Embed
from .base import BaseEmbedBuilder

class AttackBuilder(BaseEmbedBuilder):
  def __init__(self, attack: Attack) -> None:
    self.attack = attack
    self.art = attack.art
    prefix = attack.name_prefix_art or self.art.name
    self.title = self.builder.get_content(self.LANGUAGE, "attackTitle", prefix=prefix, attack=attack)
  async def build(self, page: int) -> Embed:
    description = self.attack.description
    if description is None:
      description = self.builder.safe_get_content_unknown_formatting(self.LANGUAGE, "defaultEmbedDescription")
    embed = Embed(
      title=self.title,
      description=description
    )
    if self.attack.banner is not None:
      embed.set_image(url=self.attack.banner)
    return embed