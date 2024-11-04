from morkato.work.context import MorkatoContext
from morkato.work.converters import (ConverterManager, Converter)
from morkato.work.project import registry
from morkato.state import MorkatoConnectionState
from morkato.abc import UnresolvedSnowflakeList
from morkato.utils import DATE_FORMAT
from morkato.http import HTTPClient
from morkato.ability import Ability
from morkato.family import Family
from morkato.attack import Attack
from morkato.art import Art
from datetime import datetime
from unidecode import unidecode
from discord import Interaction
from typing import (
  Optional,
  Iterator,
  TypeVar,
  Tuple,
  Union,
  Dict,
  Any
)
import app.errors
import re

T = TypeVar('T')
P = TypeVar('P')

def strip_text(
  text: str, *,
  ignore_accents: Optional[bool] = None,
  ignore_empty: Optional[bool] = None,
  case_insensitive: Optional[bool] = None,
  strip_text: Optional[bool] = None,
  empty: Optional[str]  = None
) -> str:
  if empty is None:
    empty = '-'
  if strip_text:
    text = text.strip()
  if ignore_accents:
     text = unidecode(text)
  if ignore_empty:
     text = re.sub(r'\s+', empty, text)
  if case_insensitive:
     text = text.lower()
  return text
def strip_text_all(text: str, *, empty: Optional[str] = None) -> str:
  return strip_text(
     text=text,
     ignore_accents=True,
     ignore_empty=True,
     case_insensitive=True,
     strip_text=True,
     empty=empty
  )

class BaseConverter(Converter[P, T]):
  def __init__(self, connection: MorkatoConnectionState, http: HTTPClient, converters: ConverterManager) -> None:
    self.connection = connection
    self.converters = converters
    self.http = http
  async def resolve(self, models: UnresolvedSnowflakeList[Any], /) -> None:
    if not models.already_loaded():
      await models.resolve()
_ID_REGEX = re.compile(r'([0-9]{15,20})$')
class IDConverter(BaseConverter[Union[str, int], T]):
  async def validate(self, arg: str) -> Union[str, int]:
    match = _ID_REGEX.match(arg.strip())
    if match is not None:
      return int(match.group(1))
    return arg
@registry
class AbilityConverter(IDConverter[Ability]):
  async def convert(self, ctx: Union[Interaction, MorkatoContext], arg: Union[str, int], *, abilities: UnresolvedSnowflakeList[Ability]) -> Ability:
    await self.resolve(abilities)
    if isinstance(arg, int):
      ability = abilities.get(arg)
      if ability is None:
        raise app.errors.AbilityNotFoundError(arg)
      return ability
    name = strip_text_all(arg)
    abilities = (ability for ability in abilities if strip_text_all(ability.name) == name)
    ability = next(abilities, None)
    if ability is None:
      raise app.errors.AbilityNotFoundError(arg)
    return ability
@registry
class FamilyConverter(IDConverter[Family]):
  async def convert(self, ctx: Union[Interaction, MorkatoContext], arg: Union[str, int], *, families: UnresolvedSnowflakeList[Family]) -> Family:
    await self.resolve(families)
    if isinstance(arg, int):
      family = families.get(arg)
      if family is None:
        raise app.errors.FamilyNotFoundError(arg)
      return family
    name = strip_text_all(arg)
    families = (family for family in families if strip_text_all(family.name) == name)
    family = next(families, None)
    if family is None:
      raise app.errors.FamilyNotFoundError(arg)
    return family
@registry
class ArtConverter(IDConverter[Art]):
  async def convert(self, ctx: Union[Interaction, MorkatoContext], arg: Union[str, int], *, arts: UnresolvedSnowflakeList[Art]) -> Art:
    await self.resolve(arts)
    if isinstance(arg, int):
      art = arts.get(arg)
      if art is None:
        raise app.errors.ArtNotFoundError(arg)
      return art
    name = strip_text_all(arg)
    generated = (art for art in arts if strip_text_all(art.name) == name)
    art = next(generated, None)
    if art is None:
      raise app.errors.ArtNotFoundError(arg)
    return art
@registry
class AttackConverter(IDConverter[Attack]):
  @classmethod
  def _extract_artname_attackname(cls, arg: str) -> Tuple[str, Optional[str]]:
    matcher = re.match(r'([^:\n]{2,32})(?:\s*:\s*([^:\n]{2,32}))?', arg.strip())
    if matcher is None:
      raise NotImplementedError
    primary = matcher.group(1)
    second = matcher.group(2)
    if not isinstance(primary, str):
      raise NotImplementedError
    if not isinstance(second, str):
      return (primary, None)
    return (second, primary)
  async def convert(self, ctx: Union[Interaction, MorkatoContext], arg: Union[str, int], *, attacks: Dict[str, Attack], arts: UnresolvedSnowflakeList[Art]) -> Attack:
    await self.resolve(arts)
    if isinstance(arg, int):
      attack = attacks.get(arg)
      if attack is None:
        raise app.errors.AttackNotFoundError(arg)
      return attack
    (attackname, artquery) = self._extract_artname_attackname(arg)
    art: Optional[Art] = None
    if artquery is not None:
      art = await self.converters.convert(ArtConverter, ctx, artquery, arts=arts)
    name = strip_text_all(attackname)
    all_attacks: Iterator[Attack] = iter(art._attacks.values() if art is not None else attacks.values())
    all_attacks = (attack for attack in all_attacks if strip_text_all(attack.name) == name)
    attack = next(all_attacks, None)
    if attack is None:
      raise app.errors.AttackNotFoundError(attackname)
    if art is None and next(all_attacks, None) is not None:
      raise app.errors.ManyAttackError(attack)
    return attack
@registry
class DatetimeAPIFormat(Converter[str, datetime]):
  async def convert(self, ctx: Union[MorkatoContext, Interaction], arg: str) -> datetime:
    return datetime.strptime(arg, DATE_FORMAT)