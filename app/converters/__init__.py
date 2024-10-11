from morkato.work.context import MorkatoContext
from morkato.work.converters import Converter
from morkato.work.project import registry
from morkato.state import MorkatoConnectionState
from morkato.ability import Ability
from morkato.family import Family
from morkato.http import HTTPClient
from morkato.abc import Snowflake
from morkato.guild import Guild
from unidecode import unidecode
from discord import Interaction
from typing import (
  Optional,
  TypeVar,
  Union
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
  def __init__(self, connection: MorkatoConnectionState, http: HTTPClient) -> None:
    self.connection = connection
    self.http = http
  async def get_morkato_guild(self, guild: Snowflake) -> Guild:
    morkato = self.connection.get_cached_guild(guild.id)
    if morkato is None:
      morkato = await self.connection.fetch_guild(guild.id)
    return morkato
_ID_REGEX = re.compile(r'([0-9]{15,20})$')
class IDConverter(BaseConverter[Union[str, int], T]):
  async def validate(self, arg: str) -> Union[str, int]:
    match = _ID_REGEX.match(arg.strip())
    if match is not None:
      return int(match.group(1))
    return arg
@registry
class AbilityConverter(IDConverter[Ability]):
  async def convert(self, ctx: Union[Interaction, MorkatoContext], arg: Union[str, int], *, guild: Guild) -> Ability:
    abilities = guild.abilities
    if not abilities.already_loaded():
      await abilities.resolve()
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
  async def convert(self, ctx: Union[Interaction, MorkatoContext], arg: Union[str, int], *, guild: Guild) -> Family:
    families = guild.families
    if not families.already_loaded():
      await families.resolve()
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