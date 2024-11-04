from numerize.numerize import numerize
from morkato.attack import (
  AttackFlags,
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
    AttackFlags.DEFENSIVE: "attackDefensiveLineStyle",
    AttackFlags.NOT_COUNTER_ATTACKABLE: "attackNotCounterAttackableLineStyle",
    AttackFlags.INDEFENSIBLE: "attackIndefensibleLineStyle",
    AttackFlags.UNAVOIDABLE: "attackUnavoidableLineStyle",
    AttackFlags.COUNTER_ATTACKABLE: "attackCounterAttackableLineStyle",
    AttackFlags.AREA: "attackAreaLineStyle"
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
    if self.attack.stun != 0:
      headers += self.builder.get_content(self.LANGUAGE, "attackStunLineStyle", stun=numerize(self.attack.stun)) + '\n'
    if self.attack.bleed != 0:
      headers += self.builder.get_content(self.LANGUAGE, "attackBleedingLineStyle", bleed=numerize(self.attack.bleed)) + '\n'
    if self.attack.burn != 0:
      headers += self.builder.get_content(self.LANGUAGE, "attackBurningLineStyle", burn=numerize(self.attack.burn)) + '\n'
    if self.attack.poison != 0:
      headers += self.builder.get_content(self.LANGUAGE, "attackPoisonLineStyle", poison=numerize(self.attack.poison)) + '\n'
    headers += '\n'
    if self.attack.bleed_turn != 0:
      headers += (
        self.builder.get_content(self.LANGUAGE, "attackBleedingTurnLineStyle", turn=self.attack.bleed_turn)
        if self.attack.bleed_turn == 1
        else self.builder.get_content(self.LANGUAGE, "attackBleedingTurnPluralLineStyle", turn=self.attack.bleed_turn)
      ) + '\n'
    if self.attack.burn_turn != 0:
      headers += (
        self.builder.get_content(self.LANGUAGE, "attackBurningTurnLineStyle", turn=self.attack.burn_turn)
        if self.attack.burn_turn == 1
        else self.builder.get_content(self.LANGUAGE, "attackBurningTurnPluralLineStyle", turn=self.attack.burn_turn)
      ) + '\n'
    if self.attack.poison_turn != 0:
      headers += (
        self.builder.get_content(self.LANGUAGE, "attackPoisonTurnLineStyle", turn=self.attack.poison_turn)
        if self.attack.poison_turn == 1
        else self.builder.get_content(self.LANGUAGE, "attackPoisonTurnPluralLineStyle", turn=self.attack.poison_turn)
      ) + '\n'
    headers = headers.strip('\n')
    headers += '\n\n'
    flags = (
      self.builder.get_content_unknown_formatting(self.LANGUAGE, name)
      for (key, name) in self.INTENTS_MAP_LINE_STYLE.items()
      if self.attack.flags.hasflag(key)
    )
    headers += '\n'.join(flags)
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