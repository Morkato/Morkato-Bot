from discord.embeds import Embed
from .base import BaseEmbedBuilder

class PlayerChoiceTypeBuilder(BaseEmbedBuilder):
  def __init__(self):
    self.title = self.msgbuilder.get_content(self.LANGUAGE, "playerChoiceTypeTitle")
    self.description = self.msgbuilder.get_content(self.LANGUAGE, "playerChoiceTypeDescription")
  async def build(self, page: int) -> Embed:
    return Embed(
      title = self.title,
      description = self.description
    )