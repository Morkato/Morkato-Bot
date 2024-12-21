from morkato.family import Family
from discord.embeds import Embed
from .base import BaseEmbedBuilder

class FamilyBuilder(BaseEmbedBuilder):
  def __init__(self, family: Family) -> None:
    self.ability_line_style = self.msgbuilder.get_content(self.LANGUAGE, "familyAbilityLineStyle")
    self.title = self.msgbuilder.get_content(self.LANGUAGE, "familyTitle", family=family)
    self.family = family
  async def build(self, page: int) -> Embed:
    description = self.family.description
    if description is None:
      description = self.msgbuilder.get_content(self.LANGUAGE, "defaultEmbedDescription")
    if self.family._abilities:
      description += "\n\n"
      for (idx, ability) in enumerate(self.family._abilities.values(), start=1):
        description += self.ability_line_style.format(idx=idx, ability=ability)
    embed = Embed(
      title = self.title,
      description = description
    )
    if self.family.banner is not None:
      embed.set_image(url=self.family.banner)
    return embed
  def length(self) -> int:
    return 1
class FamilyRegistryUser(FamilyBuilder):
  def __init__(self, family: Family, is_valid: bool) -> None:
    super().__init__(family)
    self.is_valid = is_valid
  async def build(self, page: int) -> Embed:
    embed = await super().build(page)
    key = "rollNotValid" if not self.is_valid else "familyRollValid"
    embed.set_footer(
      text = self.msgbuilder.get_content(self.LANGUAGE, key, family = self.family),
      icon_url = self.DEFAULT_ICON
    )
    return embed
class FamilyCreated(FamilyBuilder):
  async def build(self, page: int) -> Embed:
    embed = await super().build(page)
    embed.set_footer(
      text = self.msgbuilder.get_content(self.LANGUAGE, "familyCreated", family=self.family),
      icon_url = self.DEFAULT_ICON
    )
    return embed
class FamilyUpdated(FamilyBuilder):
  async def build(self, page: int) -> Embed:
    embed = await super().build(page)
    embed.set_footer(
      text = self.msgbuilder.get_content(self.LANGUAGE, "familyUpdated", family=self.family),
      icon_url = self.DEFAULT_ICON
    )
    return embed
class FamilyDeleted(FamilyBuilder):
  async def build(self, page: int) -> Embed:
    embed = await super().build(page)
    embed.set_footer(
      text = self.msgbuilder.get_content(self.LANGUAGE, "familyDeleted", family=self.family),
      icon_url = self.DEFAULT_ICON
    )
    return embed