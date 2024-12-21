from morkbmt.extension import (ExtensionCommandBuilder, Extension, Converter)
from morkbmt.core import registry
from morkato.abc import UnresolvedSnowflakeList
from morkato.ability import Ability
from morkato.family import Family
from morkato.attack import Attack
from morkato.art import Art
from app.embeds.base import BaseEmbedBuilder
from typing_extensions import Self
from typing import (
  Optional,
  Iterator,
  TypeVar,
  Tuple,
  Union,
  Dict
)
import app.errors
import app.utils
import discord
import re

T = TypeVar('T')

@registry
class MorkatoConfiguration(Extension):
  toattack: Converter[Attack] # Injected when :.setup: is called
  toart: Converter[Art] # Injected when :.setup: is called
  toability: Converter[Ability] # Injected when :.setup: is called
  tofamily: Converter[Family] # Injected when :.setup: is called
  user: discord.ClientUser
  async def setup(self, commands: ExtensionCommandBuilder[Self]):
    BaseEmbedBuilder.setup(self.msgbuilder, self.user.display_avatar.url)
    self.msgbuilder.from_archive("global-error.yml")
    self.msgbuilder.from_archive("rpg-commands.yml")
    self.msgbuilder.from_archive("rpg-rolls.yml")
    self.msgbuilder.from_archive("rpg-guild.yml")
    self.msgbuilder.from_archive("rpg-utility.yml")
    self.msgbuilder.from_archive("rpg-families-abilities.yml")
    self.msgbuilder.from_archive("rpg-arts-attacks.yml")
    self.msgbuilder.from_archive("rpg-players.yml")
    self.msgbuilder.from_archive("rpg-users.yml")
    self.msgbuilder.from_archive("embeds.yml")
    self.msgbuilder.from_archive("utility.yml")

_ID_REGEX = re.compile(r'([0-9]{15,20})$')
class IDConverter(Converter[T]):
  def _get_text_or_id(self, arg: str) -> Union[str, int]:
    match = _ID_REGEX.match(arg.strip())
    if match is not None:
      return int(match.group(1))
    return arg
@registry
class AbilityConverter(IDConverter[Ability]):
  async def convert(self, arg: Union[str, int], *, abilities: UnresolvedSnowflakeList[Ability]) -> Ability:
    await abilities.resolve()
    if isinstance(arg, int):
      ability = abilities.get(arg)
      if ability is None:
        raise app.errors.AbilityNotFoundError(arg)
      return ability
    name = app.utils.strip_text_all(arg)
    abilities = (ability for ability in abilities if app.utils.strip_text_all(ability.name) == name)
    ability = next(abilities, None)
    if ability is None:
      raise app.errors.AbilityNotFoundError(arg)
    return ability
@registry
class FamilyConverter(IDConverter[Family]):
  async def convert(self, arg: Union[str, int], *, families: UnresolvedSnowflakeList[Family]) -> Family:
    await families.resolve()
    if isinstance(arg, int):
      family = families.get(arg)
      if family is None:
        raise app.errors.FamilyNotFoundError(arg)
      return family
    name = app.utils.strip_text_all(arg)
    families = (family for family in families if app.utils.strip_text_all(family.name) == name)
    family = next(families, None)
    if family is None:
      raise app.errors.FamilyNotFoundError(arg)
    return family
@registry
class ArtConverter(IDConverter[Art]):
  @classmethod
  def _validate_art_name(self, name: str) -> None:
    if re.match(r'^[^:\n]{2,32}$', name) is None:
      raise app.errors.ValidationError("artNameInvalid", name=name)
  async def convert(self, arg: Union[str, int], *, arts: UnresolvedSnowflakeList[Art]) -> Art:
    await arts.resolve()
    arg = self._get_text_or_id(arg)
    if isinstance(arg, int):
      art = arts.get(arg)
      if art is None:
        raise app.errors.ArtNotFoundError(arg)
      return art
    name = app.utils.strip_text_all(arg)
    generated = (art for art in arts if app.utils.strip_text_all(art.name) == name)
    art = next(generated, None)
    if art is None:
      raise app.errors.ArtNotFoundError(arg)
    return art
@registry
class AttackConverter(IDConverter[Attack]):
  @classmethod
  def _validate_attack_name(self, name: str) -> None:
    if re.match(r'^[^:\n]{2,32}$', name) is None:
      raise app.errors.ValidationError("attackNameInvalid", name=name)
  @classmethod
  def _extract_artname_attackname(cls, arg: str) -> Tuple[str, Optional[str]]:
    art_name: Optional[str] = None
    attack_name: str
    arg = re.sub(r'\s\s+', ' ', arg)
    arg = arg.strip()
    if arg.startswith(':'):
      raise app.errors.NoActionError
    if ':' in arg:
      (art_name, attack_name) = arg.split(':', 2)
      if ':' in attack_name:
        raise app.errors.NoActionError
    else:
      attack_name = arg
    cls._validate_attack_name(attack_name)
    if art_name is not None:
      ArtConverter._validate_art_name(art_name)
    return (attack_name, art_name)
  async def convert(self, arg: Union[str, int], *, attacks: Dict[str, Attack], arts: UnresolvedSnowflakeList[Art], to_art: Converter[Art]) -> Attack:
    await arts.resolve()
    if isinstance(arg, int):
      attack = attacks.get(arg)
      if attack is None:
        raise app.errors.AttackNotFoundError(arg)
      return attack
    (attackname, artquery) = self._extract_artname_attackname(arg)
    art: Optional[Art] = None
    if artquery is not None:
      art = await to_art(artquery, arts=arts)
    name = app.utils.strip_text_all(attackname)
    all_attacks: Iterator[Attack] = iter(art._attacks.values() if art is not None else attacks.values())
    all_attacks = (attack for attack in all_attacks if app.utils.strip_text_all(attack.name) == name)
    attack = next(all_attacks, None)
    if attack is None:
      raise app.errors.AttackNotFoundError(attackname)
    if art is None and next(all_attacks, None) is not None:
      raise app.errors.ManyAttackError(attack)
    return attack