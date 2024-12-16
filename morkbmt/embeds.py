from __future__ import annotations
from typing import (
  Dict
)
from discord import (
  Interaction,
  Button,
  Embed,
  ui
)

class EmbedBuilder:
  async def build(self, page: int) -> Embed:
    raise NotImplementedError
  def length(self) -> int:
    return 1
class EmbedBuilderView(ui.View):
  ARROWLEFT = '⬅️'
  ARROWRIGHT = '➡️'
  def __init__(self, *, builder: EmbedBuilder, length: int, cache: Dict[int, Embed]) -> None:
    super().__init__(timeout=20)
    self.builder = builder
    self.length = length
    self.cache = cache
    self.current_page = 0
    if self.is_infinite():
      self.left.disabled = True
  def is_infinite(self) -> bool:
    return self.length == -1
  @ui.button(emoji=ARROWLEFT, custom_id='left')
  async def left(self, interaction: Interaction, btn: Button) -> None:
    await interaction.response.defer()
    self.current_page -= 1
    embed: Embed
    if self.is_infinite():
      if self.current_page == -1:
        self.current_page = 0
        self.left.disabled = True
        await interaction.edit_original_response(view=self)
        return
      embed = self.cache[self.current_page]
      if self.current_page == 0:
        self.left.disabled = True
      await interaction.edit_original_response(embed=embed, view=self)
      return
    if self.current_page == -1:
      self.current_page = self.length - 1
    try:
      embed = self.cache[self.current_page]
    except KeyError:
      embed = await self.builder.build(self.current_page)
    await interaction.edit_original_response(embed=embed)
  @ui.button(emoji=ARROWRIGHT, custom_id='right')
  async def right(self, interaction: Interaction, btn: Button) -> None:
    await interaction.response.defer()
    embed: Embed
    if self.is_infinite():
      try:
        self.current_page += 1
        embed = await self.builder.build(self.current_page)
        self.cache[self.current_page] = embed
      except StopAsyncIteration:
        self.length = self.current_page
        self.current_page = 0
        embed = self.cache[0]
      self.left.disabled = False
      await interaction.edit_original_response(embed=embed, view=self)
      return
    self.current_page += 1
    if self.current_page >= self.length:
      self.current_page = 0
    try:
      embed = self.cache[self.current_page]
    except KeyError:
      self.cache[self.current_page] = embed = await self.builder.build(self.current_page)
    await interaction.edit_original_response(embed=embed)