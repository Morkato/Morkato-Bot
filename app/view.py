from discord.interactions import Interaction
from morkato.player import Player
from morkato.guild import Guild
from typing import Optional
from discord import ui
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
    return await super().on_timeout()
  async def on_error(self, interaction: Interaction, error: Exception, item: ui.Item):
    try:
      self.future.set_result(None)
    except asyncio.InvalidStateError:
      pass
    return await super().on_error(interaction, error, item)
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