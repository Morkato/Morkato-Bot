from morkato.work.builder import MessageBuilder
from morkato.work.embeds import EmbedBuilder
from morkato.ability import Ability
from morkato.family import Family
from morkato.attack import Attack
from discord.embeds import Embed
from morkato.types import ArtType
from discord.user import User
from morkato.art import Art
from .types import RolledObjectModel
from typing import (
  ClassVar,
  Dict,
  List
)

class BaseEmbedBuilder(EmbedBuilder):
  LANGUAGE: str
  builder: MessageBuilder
  @classmethod
  def set_message_builder(cls, builder: MessageBuilder) -> None:
    cls.LANGUAGE = builder.PT_BR
    cls.builder = builder
class EmbedBuilderRolledObject(BaseEmbedBuilder):
  CHUNK_SIZE: ClassVar[int] = 10
  def __init__(
    self, models: List[RolledObjectModel], *,
    rolled: Dict[int, int],
    quantity: int,
    title: str,
    style: str
    ) -> None:
    self.quantity = quantity
    self.models = models
    self.rolled = rolled
    self.style = style
    self.title = title
  async def build_base_embed(self) -> Embed:
    return Embed(
      title = self.title,
      description = self.builder.safe_get_content(self.LANGUAGE, "embedBuilderRolledObjectDescription", self.quantity)
    )
  async def build(self, page: int) -> Embed:
    embed = await self.build_base_embed()
    description = embed.description
    description += '\n\n'
    start_chunk = page * self.CHUNK_SIZE
    try:
      for i in range(start_chunk, start_chunk + self.CHUNK_SIZE):
        obj = self.models[i]
        description += self.style.format(i + 1, obj.percent, obj.name, self.rolled.get(obj.id, 0))
        description += '\n'
    except IndexError:
      pass
    embed.description = description
    return embed
  def length(self) -> int:
    length = len(self.models)
    if length == 0:
      return 1
    elif length % self.CHUNK_SIZE != 0:
      return length // self.CHUNK_SIZE + 1
    return length // self.CHUNK_SIZE
class PlayerChoiceTypeBuilder(BaseEmbedBuilder):
  async def build(self, page: int) -> Embed:
    return Embed(
      title = self.builder.safe_get_content(self.LANGUAGE, "playerChoiceTypeTitle"),
      description = self.builder.safe_get_content(self.LANGUAGE, "playerChoiceTypeDescription")
    )
class AbilityBuilder(BaseEmbedBuilder):
  def __init__(self, ability: Ability) -> None:
    self.ability = ability
  async def build(self, page: int) -> Embed:
    description = self.ability.description or "No description"
    embed = Embed(
      title="Habilidade: %s" % self.ability.name,
      description=description
    )
    if self.ability.banner is not None:
      embed.set_image(url=self.ability.banner)
    return embed
  def length(self) -> int:
    return 1
class FamilyBuilder(BaseEmbedBuilder):
  def __init__(self, family: Family) -> None:
    self.family = family
  async def build(self, page: int) -> Embed:
    description = self.family.description or "No description"
    if self.family._abilities:
      description += "\n\n"
      for (idx, ability) in enumerate(self.family._abilities.values(), 1):
        description += "**%s - Habilidade: `%s`**\n" % (idx, ability.name)
    embed = Embed(
      title = f"Família: {self.family.name}",
      description=description
    )
    if self.family.banner is not None:
      embed.set_image(url=self.family.banner)
    return embed
  def length(self) -> int:
    return 1
class FamilyRegistryPlayer(FamilyBuilder):
  def __init__(self, family: Family, is_valid: bool, usr: User) -> None:
    super().__init__(family)
    self.is_valid = is_valid
    self.user = usr
  async def build(self, page: int) -> Embed:
    embed = await super().build(page)
    if not self.is_valid:
      embed.set_footer(text="Este roll não foi contabilizado, pois você não possuí mais rolls.", icon_url=self.user.display_avatar.url)
    return embed
class FamilySelectForPlayer(BaseEmbedBuilder):
  def __init__(self, usr: User, families: List[Family], selected: int) -> None:
    self.families = families
    self.selected = selected
    self.usr = usr
  async def build(self, page: int) -> Embed:
    description = f"Seleção de UMA família para: **`@{self.usr.name}`**. A escolhida será aquela no qual está em negrito.\n\n"
    selected = self.families[self.selected]
    for (idx, family) in enumerate(self.families):
      if idx == self.selected:
        description += "> **%s - Família: %s**\n" % (idx + 1, family.name)
        continue
      description += "**%s** - Família: %s\n" % (idx + 1, family.name)
    embed = Embed(
      title = "Seleção de família",
      description = description
    )
    if selected.banner is not None:
      embed.set_image(url = selected.banner)
    embed.set_footer(text = "Você selecionou: %s" % selected.name)
    return embed
  def length(self):
    return 1
class AbilityRegistryPlayer(AbilityBuilder):
  def __init__(self, ability: Ability, is_valid: bool, icon: str) -> None:
    super().__init__(ability)
    self.is_valid = is_valid
    self.icon = icon
  async def build(self, page: int) -> Embed:
    embed = await super().build(page)
    if not self.is_valid:
      embed.set_footer(
        text = "Este roll não foi contabilizado, pois você não possuí mais rolls.",
        icon_url = self.icon
      )
    return embed
class ArtBuilder(BaseEmbedBuilder):
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
class AttackBuilder(BaseEmbedBuilder):
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