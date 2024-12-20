from .base import BaseEmbedBuilder
from discord.embeds import Embed
from discord.user import User

class UserRegistryEmbed(BaseEmbedBuilder):
  def __init__(self, author: User) -> None:
    self.author = author
  def build(self, page: int) -> Embed:
    title = self.msgbuilder.get_content(self.LANGUAGE, "userRegistryTitle")
    description = self.msgbuilder.get_content(self.LANGUAGE, "userRegistryDescription", author=self.author)
    return Embed(
      title = title,
      description = description
    )