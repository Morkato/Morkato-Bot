from __future__ import annotations
from morkato.ext.context import MorkatoContext
from .errors import ArtNotFoundError
from morkato.attack import Attack
from unidecode import unidecode
from morkato.guild import Guild
from morkato.art import Art
import re
from discord.ext.commands import (
  IDConverter
)
from typing import (
  Optional,
  Tuple
)

def strip_text(text: str, *, ignore_accents: Optional[bool] = None, ignore_empty: Optional[bool] = None, case_insensitive: Optional[bool] = None, strip_text: Optional[bool] = None, empty: Optional[str]  = None) -> str:
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

class ArtConverter(IDConverter[Art]):
  def _get_art_by_name(self, guild: Guild, name: str) -> Optional[Art]:
    name = strip_text_all(name)
    arts = (art for art in guild.arts if strip_text_all(art.name) == name)
    return next(arts, None)
  async def _get_art_by_guild(self, guild: Guild, arg: str) -> Art:
    id = self._get_id_match(arg)
    if id is not None:
      id = int(id.group(1))
      art = guild.arts.get(id)
      if art is None:
        raise ArtNotFoundError(str(id))
      return art
    art = self._get_art_by_name(guild, arg)
    if art is None:
      raise ArtNotFoundError(arg)
    return art
  async def convert(self, ctx: MorkatoContext, arg: str) -> Art:
    if not ctx.morkato_guild.arts.already_loaded():
      await ctx.morkato_guild.arts.resolve()
    return await self._get_art_by_guild(ctx.morkato_guild, arg)
class AttackConverter(IDConverter[Attack]):
  @classmethod
  def _extract_artname_attackname(cls, arg: str) -> Tuple[str, Optional[str]]:
    matcher = re.match(r'([^:\n]{2,32})(?:\s*:\s*([^:\n]{2,32}))?', arg.strip())
    if matcher is None:
      raise NotImplementedError
    primary = matcher.group(1)
    second = matcher.group(2)
    if not isinstance(primary, str):
      raise NotADirectoryError
    if not isinstance(second, str):
      return (primary, None)
    return (second, primary)
  def _get_next_attack_by_name(self, guild: Guild, name: str) -> Optional[Attack]:
    name = strip_text_all(name)
    attacks = (attack for attack in guild._attacks.values() if strip_text_all(attack.name) == name)
    return next(attacks, None)
  def _get_attack_by_name(self, guild: Guild, name: str, *, art: Optional[Art] = None) -> Optional[Attack]:
    name = strip_text_all(name)
    attacks = art._attacks.values() if art is not None else guild._attacks.values()
    attacks = (attack for attack in attacks if strip_text_all(attack.name) == name)
    attack = next(attacks, None)
    if attack is None:
      return None
    elif art is not None:
      return attack
    other = next(attacks, None)
    if other is not None:
      raise NotImplementedError
    return attack
  async def _get_attack_by_guild(self, guild: Guild, arg: str) -> Attack:
    id = self._get_id_match(arg)
    if id is not None:
      id = int(id.group(1))
      attack = guild.get_attack(id)
      if attack is None:
        raise NotImplementedError
      return attack
    (attackname, artquery) = self._extract_artname_attackname(arg)
    art: Optional[Art] = None
    if artquery is not None:
      art = await ArtConverter()._get_art_by_guild(guild, artquery)
    attack = self._get_attack_by_name(guild, attackname, art=art)
    if attack is None:
      raise NotImplementedError
    return attack
  async def convert(self, ctx: MorkatoContext, arg: str) -> Attack:
    if not ctx.morkato_guild.arts.already_loaded():
      await ctx.morkato_guild.arts.resolve()
    return await self._get_attack_by_guild(ctx.morkato_guild, arg)