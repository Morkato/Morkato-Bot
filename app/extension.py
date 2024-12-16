from morkato.work.context import EmbedBuilderView
from morkato.work.msgbuilder import MessageBuilder
from morkato.work.embeds import EmbedBuilder
from morkato.work.extension import Extension
from morkato.state import MorkatoConnectionState
from morkato.guild import Guild
from morkato.http import HTTPClient
from morkato.player import Player
from morkato.abc import Snowflake
from typing import (
  TypeVar,
  Dict
)
import discord

T = TypeVar('T')
P = TypeVar('P')

class BaseExtension(Extension):
  connection: MorkatoConnectionState
  user: discord.ClientUser
  http: HTTPClient
  async def get_morkato_guild(self, guild: Snowflake) -> Guild:
    morkato = self.connection.get_cached_guild(guild.id)
    if morkato is None:
      morkato = await self.connection.fetch_guild(guild.id)
    return morkato
  async def send_confirmation(self, interaction: discord.Interaction, **options) -> bool:
    view = ConfirmationView()
    if interaction.response.is_done():
      await interaction.edit_original_response(view=view, **options)
    else:
      await interaction.response.send_message(view=view, **options)
    return await view.get_value()
  async def send_embed(self, interaction: discord.Interaction, builder: EmbedBuilder, *, resolve_all: bool = False, wait: bool = True) -> None:
    cache: Dict[int, discord.Embed] = {}
    length = builder.length()
    if length == 0:
      raise NotImplementedError
    embed = await builder.build(0)
    if interaction.is_expired():
      return
    if interaction.response.is_done():
      await interaction.edit_original_response(embed=embed)
    else:
      await interaction.response.send_message(embed=embed)
    if length == 1:
      return
    cache[0] = embed
    if resolve_all and length != -1:
      cache |= {
        idx: await builder.build(idx)
        for idx in range(1, length)
      }
    view = EmbedBuilderView(
      builder=builder,
      length=length,
      cache=cache
    )
    await interaction.edit_original_response(view=view)
    if wait:
      await view.wait()
  async def get_cached_or_fetch_player(self, guild: Guild, id: int) -> Player:
    player = guild.get_cached_player(id)
    if player is None:
      player = await guild.fetch_player(id)
    return player
class ConfirmationView(discord.ui.View):
  CHECK = '✅'
  UNCHECK = '❌'
  def __init__(self) -> None:
    super().__init__(timeout=20)
    self.confirmed = False
  async def get_value(self) -> bool:
    await self.wait()
    return self.confirmed
  @discord.ui.button(emoji=CHECK, custom_id="check")
  async def check(self, interaction: discord.Interaction, btn: discord.ui.Button) -> None:
    await interaction.response.defer()
    self.confirmed = True
    self.stop()
  @discord.ui.button(emoji=UNCHECK, custom_id="uncheck")
  async def uncheck(self, interaction: discord.Interaction, btn: discord.ui.Button) -> None:
    await interaction.response.defer()
    self.stop()