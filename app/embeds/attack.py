from numerize.numerize import numerize
from morkato.attack import (
  AttackIntents,
  Attack
)
from discord.embeds import Embed
from typing import (
  ClassVar,
  Dict
)
from .base import BaseEmbedBuilder

class AttackBuilder(BaseEmbedBuilder):
  INTENTS_MAP_LINE_STYLE: ClassVar[Dict[int, str]] = {
    AttackIntents.DEFENSIVE: "attackDefensiveLineStyle",
    AttackIntents.NOT_COUNTER_ATTACKABLE: "attackNotCounterAttackableLineStyle",
    AttackIntents.INDEFENSIBLE: "attackIndefensibleLineStyle",
    AttackIntents.UNAVOIDABLE: "attackUnavoidableLineStyle",
    AttackIntents.COUNTER_ATTACKABLE: "attackCounterAttackableLineStyle",
    AttackIntents.AREA: "attackAreaLineStyle"
  }
  def __init__(self, attack: Attack) -> None:
    self.attack = attack
    self.art = attack.art
    prefix = attack.name_prefix_art or self.art.name
    self.title = self.builder.get_content(self.LANGUAGE, "attackTitle", prefix=prefix, attack=attack)
  def get_headers(self) -> str:
    headers = (
      self.builder.get_content_unknown_formatting(self.LANGUAGE, "attackDamageEmptyLineStyle")
      if self.attack.damage == 0
      else self.builder.get_content(self.LANGUAGE, "attackDamageLineStyle", damage=numerize(self.attack.damage))
    ) + '\n'
    if self.art.type in (self.art.RESPIRATION, self.art.FIGHTING_STYLE):
      headers += (
        self.builder.get_content_unknown_formatting(self.LANGUAGE, "attackBreathEmptyLineStyle")
        if self.attack.breath == 0
        else self.builder.get_content(self.LANGUAGE, "attackBreathLineStyle", breath=numerize(self.attack.breath))
      ) + '\n'
    if self.art.type in (self.art.KEKKIJUTSU, self.art.FIGHTING_STYLE):
      headers += (
        self.builder.get_content_unknown_formatting(self.LANGUAGE, "attackBloodEmptyLineStyle")
        if self.attack.blood == 0
        else self.builder.get_content(self.LANGUAGE, "attackBloodLineStyle", blood=numerize(self.attack.blood))
      ) + '\n'
    headers += '\n'
    intents = (
      self.builder.get_content_unknown_formatting(self.LANGUAGE, name)
      for (key, name) in self.INTENTS_MAP_LINE_STYLE.items()
      if self.attack.intents.has_intent(key)
    )
    headers += '\n'.join(intents)
    return headers.strip('\n')
  async def build(self, page: int) -> Embed:
    description = self.attack.description
    if description is None:
      description = self.builder.safe_get_content_unknown_formatting(self.LANGUAGE, "defaultEmbedDescription")
    description += "\n\n"
    description += self.get_headers()
    embed = Embed(
      title=self.title,
      description=description
    )
    if self.attack.banner is not None:
      embed.set_image(url=self.attack.banner)
    return embed
class AttackCreatedBuilder(AttackBuilder):
  def __init__(self, attack: Attack) -> None:
    super().__init__(attack)
    self.footer_text = self.builder.safe_get_content(self.LANGUAGE, "attackCreated", attack=attack)
  async def build(self, page: int) -> Embed:
    embed = await super().build(page)
    embed.set_footer(
      text = self.footer_text,
      icon_url = self.DEFAULT_ICON
    )
    return embed
class AttackUpdatedBuilder(AttackBuilder):
  def __init__(self, attack: Attack) -> None:
    super().__init__(attack)
    self.footer_text = self.builder.safe_get_content(self.LANGUAGE, "attackUpdated", attack=attack)
  async def build(self, page: int) -> Embed:
    embed = await super().build(page)
    embed.set_footer(
      text = self.footer_text,
      icon_url = self.DEFAULT_ICON
    )
    return embed