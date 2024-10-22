from numerize.numerize import numerize
from discord.colour import Colour
from discord.embeds import Embed
from morkato.npc import Npc
from itertools import chain
from .base import BaseEmbedBuilder

class NpcCardBuilder(BaseEmbedBuilder):
  def __init__(self, npc: Npc) -> None:
    self.npc = npc
    self.author_name: str
    if npc.type == npc.HUMAN:
      self.author_name = self.builder.get_content(self.LANGUAGE, "npcHumanPresent", npc=npc, life=numerize(npc.max_life), breath=numerize(npc.max_breath))
    elif npc.type == npc.ONI:
      self.author_name = self.builder.get_content(self.LANGUAGE, "npcOniPresent", npc=npc, life=numerize(npc.max_life), blood=numerize(npc.max_blood))
    elif npc.type == npc.HYBRID:
      self.author_name = self.builder.get_content(self.LANGUAGE, "npcHybridPresent", npc=npc, life=numerize(npc.max_life), breath=numerize(npc.max_breath), blood=numerize(npc.max_blood))
    flags = npc.flags
    prodigyKey = "npcProdigyIsValidLineStyle" if flags.prodigy else "npcProdigyIsNotValidLineStyle"
    description = ''
    description += self.builder.get_content(self.LANGUAGE, "npcFamilyLineStyle", npc=npc) + '\n'
    description += self.builder.get_content(self.LANGUAGE, "npcEnergyLineStyle", npc=npc) + '\n'
    description += self.builder.get_content_unknown_formatting(self.LANGUAGE, prodigyKey) + '\n'
    if self.npc.type in (self.npc.HUMAN, self.npc.HYBRID):
      markKey = "npcMarkIsValidLineStyle" if flags.mark else "npcMarkIsNotValidLineStyle"
      description += self.builder.get_content_unknown_formatting(self.LANGUAGE, markKey) + '\n'
    if self.npc.type in (self.npc.ONI, self.npc.HYBRID):
      berserkKey = "npcBerserkIsValidLineStyle" if flags.berserk else "npcBerserkIsNotValidLineStyle"
      description += self.builder.get_content_unknown_formatting(self.LANGUAGE, berserkKey) + '\n'
    description += self.builder.get_content_unknown_formatting(self.LANGUAGE, "npcAbilitiesPresent") + "\n\n"
    self.description = description
    self.abilities_line_style = self.builder.get_content_unknown_formatting(self.LANGUAGE, "npcAbilitiesLineStyle")
  def get_color(self) -> int:
    if self.npc.type == self.npc.HUMAN:
      return Colour.from_rgb(0, 255, 0)
    elif self.npc.type == self.npc.ONI:
      return Colour.from_rgb(255, 0, 0)
    return Colour.from_rgb(0, 0, 255)
  async def build(self, page: int) -> Embed:
    embed = Embed(colour=self.get_color())
    embed.set_author(
      name = self.author_name,
      icon_url = self.npc.icon
    )
    abilities = chain(self.npc.family._abilities.values(), self.npc._abilities.values())
    description = self.description
    description += '\n'.join(self.abilities_line_style.format(idx=idx, ability=ability) for (idx, ability) in enumerate(abilities, start=1))
    embed.description = description
    return embed