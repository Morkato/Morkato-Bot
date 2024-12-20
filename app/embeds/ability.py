from morkato.ability import Ability
from discord.embeds import Embed
from .base import BaseEmbedBuilder
from typing import Dict

class AbilityRollMeBuilder(BaseEmbedBuilder):
  def __init__(self, rolled_abilities: Dict[int, Ability]) -> None:
    self.abilities = rolled_abilities
  async def build(self, page: int) -> Embed:
    title = self.msgbuilder.get_content(self.LANGUAGE, "abilityUserTitle")
    style = self.msgbuilder.get_content(self.LANGUAGE, "abilityUserLineStyle")
    description = ''
    for (idx, ability) in enumerate(self.abilities.values(), start=1):
      description += style.format(idx=idx, ability=ability)
      description += '\n'
    return Embed(
      title = title,
      description = description
    )
class AbilityBuilder(BaseEmbedBuilder):
  def __init__(self, ability: Ability) -> None:
    self.title = self.msgbuilder.get_content(self.LANGUAGE, "abilityTitle", ability=ability)
    self.ability = ability
  async def build(self, page: int) -> Embed:
    description = self.ability.description
    if description is None:
      description = self.msgbuilder.get_content(self.LANGUAGE, "defaultEmbedDescription")
    embed = Embed(
      title=self.title,
      description=description
    )
    if self.ability.banner is not None:
      embed.set_image(url=self.ability.banner)
    return embed
class AbilityRegistryUser(AbilityBuilder):
  def __init__(self, ability: Ability, is_valid: bool) -> None:
    super().__init__(ability)
    self.is_valid = is_valid
  async def build(self, page: int) -> Embed:
    embed = await super().build(page)
    key = "rollNotValid" if not self.is_valid else "abilityRollValid"
    embed.set_footer(
      text = self.msgbuilder.get_content(self.LANGUAGE, key, ability = self.ability),
      icon_url = self.DEFAULT_ICON
    )
    return embed
class AbilityCreated(AbilityBuilder):
  async def build(self, page: int) -> Embed:
    embed = await super().build(page)
    embed.set_footer(
      text = self.msgbuilder.get_content(self.LANGUAGE, "abilityCreated", ability=self.ability),
      icon_url = self.DEFAULT_ICON
    )
    return embed
class AbilityUpdated(AbilityBuilder):
  async def build(self, page: int) -> Embed:
    embed = await super().build(page)
    embed.set_footer(
      text = self.msgbuilder.get_content(self.LANGUAGE, "abilityUpdated", ability=self.ability),
      icon_url = self.DEFAULT_ICON
    )
    return embed
class AbilityDeleted(AbilityBuilder):
  async def build(self, page: int) -> Embed:
    embed = await super().build(page)
    embed.set_footer(
      text = self.msgbuilder.get_content(self.LANGUAGE, "abilityDeleted", ability=self.ability),
      icon_url = self.DEFAULT_ICON
    )
    return embed