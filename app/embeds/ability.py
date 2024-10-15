from morkato.ability import Ability
from discord.embeds import Embed
from .base import BaseEmbedBuilder

class AbilityBuilder(BaseEmbedBuilder):
  def __init__(self, ability: Ability) -> None:
    self.title = self.builder.get_content("abilityTitle", ability=ability)
    self.ability = ability
  async def build(self, page: int) -> Embed:
    description = self.ability.description
    if description is None:
      description = self.builder.safe_get_content_unknown_formatting(self.LANGUAGE, "defaultEmbedDescription")
    embed = Embed(
      title=self.title,
      description=description
    )
    if self.ability.banner is not None:
      embed.set_image(url=self.ability.banner)
    return embed
class AbilityRegistryPlayer(AbilityBuilder):
  def __init__(self, ability: Ability, is_valid: bool) -> None:
    super().__init__(ability)
    self.is_valid = is_valid
  async def build(self, page: int) -> Embed:
    embed = await super().build(page)
    if not self.is_valid:
      embed.set_footer(
        text = self.builder.safe_get_content_unknown_formatting(self.LANGUAGE, "rollNotValid"),
        icon_url = self.DEFAULT_ICON
      )
    return embed