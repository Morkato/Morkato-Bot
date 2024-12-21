from morkbmt.extension import (ExtensionCommandBuilder, Converter, command)
from morkbmt.context import MorkatoContext
from morkbmt.core import registry
from morkato.abc import UnresolvedSnowflakeList
from morkato.attack import Attack
from morkato.art import (ArtType, Art)
from app.extension import BaseExtension
from typing_extensions import Self
from typing import (
  Coroutine,
  Callable,
  ClassVar,
  Optional,
  Dict,
  List,
  Any
)
from enum import Enum
import app.embeds
import app.errors
import app.utils

class ArtOption(Enum):
  GET = "get"
  LIST = "list"
@registry
class RPGCommands(BaseExtension):
  RESPIRATION_KEYS: ClassVar[List[str]] = ["resp", "respiration"]
  KEKKIJUTSU_KEYS: ClassVar[List[str]] = ["kekki", "kekkijutsu"]
  FIGHTING_STYLE_KEYS: ClassVar[List[str]] = ["fight", "fighting-style", "fight-style"]
  toattack: Converter[Attack]
  toart: Converter[Art]
  async def setup(self, commands: ExtensionCommandBuilder[Self]) -> None:
    self.LANGUAGE = self.msgbuilder.PT_BR
    self.ART_OPTIONS_HANDLERS: Dict[ArtOption, Callable[..., Coroutine[Any, Any, Any]]] = {
      ArtOption.GET: self.on_art_get,
      ArtOption.LIST: self.on_art_list
    }
    art = commands.command("art", self.art)
    attack = commands.command("attack", self.attack, aliases=['a'])
    commands.guild_only(art)
    commands.guild_only(attack)
  def extract_art_type(self, query: str) -> ArtType:
    (opt, *args) = query.split(' ')
    if args:
      raise app.errors.NoActionError
    opt = app.utils.strip_text_all(opt)
    if opt in self.RESPIRATION_KEYS:
      return Art.RESPIRATION
    if opt in self.KEKKIJUTSU_KEYS:
      return Art.KEKKIJUTSU
    if opt in self.FIGHTING_STYLE_KEYS:
      return Art.FIGHTING_STYLE
    raise app.errors.NoActionError
  async def on_art_get(self, ctx: MorkatoContext, query: str, *, arts: UnresolvedSnowflakeList[Art]) -> None:
    art = await self.toart(query, arts=arts)
    builder = app.embeds.ArtBuilder(art)
    await ctx.send_embed(builder, resolve_all=True)
  async def on_art_list(self, ctx: MorkatoContext, query: str, *, arts: UnresolvedSnowflakeList[Art]) -> None:
    by_type = self.extract_art_type(query)
    by_type_arts = (art for art in arts if art.type == by_type)
    await ctx.send_select_menu(
      models = sorted(by_type_arts, key=lambda art: len(art.name)),
      title = self.msgbuilder.get_content(self.LANGUAGE, "selectMenuArtTitle"),
      description = self.msgbuilder.get_content(self.LANGUAGE, "selectMenuArtDescription"),
      selected_line_style = self.msgbuilder.get_content(self.LANGUAGE, "selectMenuArtSelectedLineStyle"),
      line_style = self.msgbuilder.get_content(self.LANGUAGE, "selectMenuArtLineStyle"),
      key = lambda art: app.embeds.ArtBuilder(art)
    )
  async def art(self, ctx: MorkatoContext, opt: Optional[ArtOption], *, art_query: str) -> None:
    if opt is None:
      opt = ArtOption.GET
    guild = await self.get_morkato_guild(ctx.guild)
    handler = self.ART_OPTIONS_HANDLERS[opt]
    await guild.arts.resolve()
    await handler(ctx, art_query, arts=guild.arts)
  async def attack(self, ctx: MorkatoContext, *, attack_query: str) -> None:
    guild = await self.get_morkato_guild(ctx.guild)
    attack = await self.toattack(attack_query, arts=guild.arts, attacks=guild._attacks, to_art=self.toart)
    builder = app.embeds.AttackBuilder(attack)
    await ctx.send_embed(builder, resolve_all=True)