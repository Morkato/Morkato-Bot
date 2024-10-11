from discord.interactions import Interaction
from .embeds import FamilySelectForPlayer
from morkato.family import Family
from morkato.player import Player
from morkato.guild import Guild
from typing import Optional
from discord.user import User
from discord import ui
from typing import (
  List
)
import asyncio

class RegistryPlayerUi(ui.View):
  def __init__(self, guild: Guild, loop: asyncio.AbstractEventLoop) -> None:
    super().__init__(timeout=20)
    self.future: asyncio.Future[Optional[Player]] = loop.create_future()
    self.guild = guild
  def get(self) -> asyncio.Future[Optional[Player]]:
    return self.future
  async def on_timeout(self) -> None:
    try:
      self.future.set_result(None)
    except asyncio.InvalidStateError:
      pass
    return super().on_timeout()
  async def on_error(self, interaction: Interaction, error: Exception, item: ui.Item):
    try:
      self.future.set_result(None)
    except asyncio.InvalidStateError:
      pass
    return super().on_error(interaction, error, item)
  @ui.button(emoji='👨', custom_id="HUMAN")
  async def human_choice(self, interaction: Interaction, btn: ui.Button) -> None:
    await interaction.response.defer()
    player = await self.guild.create_player(interaction.user, "HUMAN")
    self.future.set_result(player)
    self.clear_items()
    self.stop()
  @ui.button(emoji='👹', custom_id="ONI")
  async def oni_choice(self, interaction: Interaction, btn: ui.Button) -> None:
    await interaction.response.defer()
    player = await self.guild.create_player(interaction.user, "ONI")
    self.future.set_result(player)
    self.clear_items()
    self.stop()
class FamilySelectForPlayerUi(ui.View):
  def __init__(self, usr: User, families: List[Family]) -> None:
    super().__init__()
    self.families = families
    self.length = len(families)
    self.usr = usr
    self.selected = 0
  @ui.button(emoji='✅', custom_id="check")
  async def check(self, interaction: Interaction, btn: ui.Button) -> None:
    pass
  @ui.button(emoji='⬇️', custom_id="arrowdown")
  async def arrowdown(self, interaction: Interaction, btn: ui.Button) -> None:
    await interaction.response.defer()
    if self.selected >= self.length - 1:
      self.selected = 0
    else:
      self.selected += 1
    embed = await FamilySelectForPlayer(self.usr, self.families, self.selected).build(0)
    await interaction.edit_original_response(embed=embed)
  @ui.button(emoji='⬆️', custom_id="arrowup")
  async def arrowup(self, interaction: Interaction, btn: ui.Button) -> None:
    await interaction.response.defer()
    if self.selected == 0:
      self.selected = self.length - 1
    else:
      self.selected -= 1
    embed = await FamilySelectForPlayer(self.usr, self.families, self.selected).build(0)
    await interaction.edit_original_response(embed=embed)