from morkato.work.extension import (Converter, command)
from morkato.work.context import MorkatoContext
from morkato.work.core import registry
from morkato.abc import UnresolvedSnowflakeList
from morkato.guild import Guild
from morkato.art import (ArtType, Art)
from morkato.npc import Npc
from app.extension import BaseExtension
from datetime import (datetime, timedelta)
from typing import (Callable, ClassVar, Optional, Dict, List)
from enum import Enum
import app.embeds
import app.errors

class ArtOption(Enum):
  GET = "get"
  LIST = "list"
class TrainOption(Enum):
  TRAIN = "train"
  NOTRAIN = "notrain"
@registry
class RPGCommands(BaseExtension):
  RESPIRATION_KEYS: ClassVar[List[str]] = ["resp", "respiration"]
  KEKKIJUTSU_KEYS: ClassVar[List[str]] = ["kekki", "kekkijutsu"]
  FIGHTING_STYLE_KEYS: ClassVar[List[str]] = ["fight", "fighting-style", "fight-style"]
  ENERGY_PEER: ClassVar[int] = 72
  LANGUAGE: ClassVar[str]
  toart: Converter[Art]
  async def setup(self) -> None:
    self.LANGUAGE = self.msgbuilder.PT_BR
    self.TRAIN_OPTIONS_HANDLERS: Dict[TrainOption, Callable[..., None]] = {
      TrainOption.TRAIN: self.on_train_train,
      TrainOption.NOTRAIN: self.on_train_notrain
    }
    self.ART_OPTIONS_HANDLERS: Dict[ArtOption, Callable[..., None]] = {
      ArtOption.GET: self.on_art_get,
      ArtOption.LIST: self.on_art_list
    }
  def release(self, current_time: datetime, npc: Npc) -> int:
    last_action = npc.last_action
    if last_action is None:
      if npc.max_energy == npc.energy:
        raise app.errors.NoActionError
      return npc.max_energy
    if npc.energy >= npc.max_energy:
      raise app.errors.NoActionError
    difference = int(timedelta.total_seconds(current_time - last_action))
    total_points = difference // self.ENERGY_PEER
    total_energy = npc.energy + total_points
    if total_energy > npc.max_energy:
      return npc.max_energy
    return total_energy
  def extract_art_type(self, query: str) -> ArtType:
    (opt, *args) = query.split(' ')
    if args:
      raise app.errors.NoActionError
    opt = app.converters.strip_text_all(opt)
    if opt in self.RESPIRATION_KEYS:
      return Art.RESPIRATION
    if opt in self.KEKKIJUTSU_KEYS:
      return Art.KEKKIJUTSU
    if opt in self.FIGHTING_STYLE_KEYS:
      return Art.FIGHTING_STYLE
    raise app.errors.NoActionError
  async def on_train_train(self, ctx: MorkatoContext, query: str, *, guild: Guild, arts: UnresolvedSnowflakeList[Art]) -> None:
    player = await self.get_cached_or_fetch_player(guild, ctx.author.id)
    npc = player.npc
    if npc is None:
      raise app.errors.NoActionError
    art = await self.convert(app.converters.ArtConverter, ctx, query, arts=guild.arts)
    current_energy = npc.energy
    current_time = datetime.now()
    if art.energy > current_energy:
      current_energy = self.release(current_time, npc)
      if art.energy > current_energy:
        raise app.errors.AppError("energyIs")
    last_action = int(current_time.timestamp() * 1000)
    energy = current_energy - art.energy
    life = art.life + npc.max_life
    breath = art.breath + npc.max_breath
    blood = art.blood + npc.max_blood
    await npc.update(
      max_life = life,
      max_breath = breath,
      max_blood = blood,
      energy = energy,
      last_action = last_action
    )
    builder = app.embeds.PlayerArtTrainBuilder(player, npc, art)
    await ctx.send_embed(builder, resolve_all=True)
  async def on_train_notrain(self, ctx: MorkatoContext, query: str, *, guild: Guild, arts: UnresolvedSnowflakeList[Art]) -> None:
    art = await self.convert(app.converters.ArtConverter, ctx, query, arts=arts)
    builder = app.embeds.ArtTrainBuilder(art)
    await ctx.send_embed(builder, resolve_all=True)
  async def on_art_get(self, ctx: MorkatoContext, query: str, *, arts: UnresolvedSnowflakeList[Art]) -> None:
    art = await self.toart(query, arts=arts)
    builder = app.embeds.ArtBuilder(art)
    await ctx.send_embed(builder, resolve_all=True)
  async def on_art_list(self, ctx: MorkatoContext, query: str, *, arts: UnresolvedSnowflakeList[Art]) -> None:
    by_type = self.extract_art_type(query)
    by_type_arts = (art for art in arts if art.type == by_type)
    await ctx.send_select_menu(
      models = sorted(by_type_arts, key=lambda art: len(art.name)),
      title = self.builder.get_content_unknown_formatting(self.LANGUAGE, "selectMenuArtTitle"),
      description = self.builder.get_content_unknown_formatting(self.LANGUAGE, "selectMenuArtDescription"),
      selected_line_style = self.builder.get_content_unknown_formatting(self.LANGUAGE, "selectMenuArtSelectedLineStyle"),
      line_style = self.builder.get_content_unknown_formatting(self.LANGUAGE, "selectMenuArtLineStyle"),
      key = lambda art: app.embeds.ArtBuilder(art)
    )
  @command(name="train")
  async def train(self, ctx: MorkatoContext, opt: Optional[TrainOption], *, art_query: str) -> None:
    if opt is None:
      opt = TrainOption.TRAIN
    guild = await self.get_morkato_guild(ctx.guild)
    handler = self.TRAIN_OPTIONS_HANDLERS[opt]
    await guild.arts.resolve()
    await handler(ctx, art_query, guild=guild, arts=guild.arts)
  @command(name="art")
  async def art(self, ctx: MorkatoContext, opt: Optional[ArtOption], *, art_query: str) -> None:
    if opt is None:
      opt = ArtOption.GET
    guild = await self.get_morkato_guild(ctx.guild)
    handler = self.ART_OPTIONS_HANDLERS[opt]
    await guild.arts.resolve()
    await handler(ctx, art_query, arts=guild.arts)