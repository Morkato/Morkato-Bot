from __future__ import annotations
from typing import (
  Optional,
  Callable,
  Generic,
  TypeVar
)
from .types import (SelectMenuObject, ArrayType)
from .embeds import EmbedBuilder
from discord import (
  Interaction,
  Embed,
  ui
)
import asyncio

SelectMenuObjectT = TypeVar('SelectMenuObjectT', bound=SelectMenuObject)

class SelectMenuEmbed(EmbedBuilder, Generic[SelectMenuObjectT]):
  def __init__(
    self, models: ArrayType[SelectMenuObjectT], *,
    title: Optional[str] = None,
    description: str,
    line_style: str,
    selected_line_style: str
  ) -> None:
    self.models = models
    self.models_length = len(models)
    self.selected = 0
    self.title = title
    self.description = description
    self.line_style = line_style
    self.selected_line_style = selected_line_style
  def get_model(self) -> SelectMenuObjectT:
    return self.models[self.selected]
  def select(self, idx: int) -> None:
    if not idx in range(0, self.models_length):
      raise ValueError("%s index out te range!" % idx)
    self.selected = idx
  def build_base_embed(self) -> Embed:
    selected = self.models[self.selected]
    embed = Embed(
      title = self.title,
      description = self.description
    )
    if selected.banner is not None:
      embed.set_image(url = selected.banner)
    return embed
  async def build(self, page: int) -> Embed:
    embed = self.build_base_embed()
    description = embed.description
    description += "\n\n"
    for (idx, model) in enumerate(self.models):
      style = self.line_style
      if idx == self.selected:
        style = self.selected_line_style
      description += style.format(idx=idx + 1, model=model)
      description += '\n'
    embed.description = description
    return embed
  def length(self) -> int:
    return 1
class SelectMenuView(ui.View, Generic[SelectMenuObjectT]):
  ARROWUP = '⬆️'
  ARROWDOWN = '⬇️'
  CHECK = '✅'
  UNCHECK = '❌'
  def __init__(self, paged: SelectMenuEmbed[SelectMenuObjectT], loop: asyncio.AbstractEventLoop, sub_builder: Callable[[SelectMenuObjectT], EmbedBuilder], /) -> None:
    super().__init__()
    self.future: asyncio.Future[SelectMenuObjectT] = loop.create_future()
    self.sub_builder = sub_builder
    self.selected = False
    self.paged = paged
    self.uncheck.disabled = True
  def get(self) -> asyncio.Future[SelectMenuObjectT]:
    return self.future
  async def on_error(self, interaction: Interaction, error: Exception, item: ui.Item):
    self.future.cancel()
    return await super().on_error(interaction, error, item)
  def on_timeout(self):
    self.future.cancel()
  @ui.button(emoji=CHECK, custom_id="check")
  async def check(self, interaction: Interaction, btn: ui.Button) -> None:
    if not self.selected:
      await interaction.response.defer()
      model = self.paged.get_model()
      builder = self.sub_builder(model)
      embed = await builder.build(0)
      self.selected = True
      self.uncheck.disabled = False
      self.arrowdown.disabled = True
      self.arrowup.disabled = True
      await interaction.edit_original_response(embed=embed, view=self)
      return
    model = self.paged.get_model()
    self.future.set_result(model)
    self.clear_items()
    self.stop()
  @ui.button(emoji=UNCHECK, custom_id="uncheck")
  async def uncheck(self, interaction: Interaction, btn: ui.Button) -> None:
    await interaction.response.defer()
    btn.disabled = True
    self.arrowdown.disabled = False
    self.arrowup.disabled = False
    if not self.selected:
      return
    self.selected = False
    embed = await self.paged.build(0)
    await interaction.edit_original_response(embed=embed, view=self)
  @ui.button(emoji=ARROWDOWN, custom_id="arrowdown")
  async def arrowdown(self, interaction: Interaction, btn: ui.Button) -> None:
    if self.selected:
      self.arrowdown.disabled = True
      self.arrowup.disabled = True
      await interaction.response.edit_message(view=self)
      return
    await interaction.response.defer()
    selected = self.paged.selected
    length = self.paged.models_length
    if selected >= length - 1:
      selected = 0
    else:
      selected += 1
    self.paged.select(selected)
    embed = await self.paged.build(0)
    await interaction.edit_original_response(embed=embed)
  @ui.button(emoji=ARROWUP, custom_id="arrowup")
  async def arrowup(self, interaction: Interaction, btn: ui.Button) -> None:
    if self.selected:
      self.arrowdown.disabled = True
      self.arrowup.disabled = True
      await interaction.response.edit_message(view=self)
      return
    await interaction.response.defer()
    selected = self.paged.selected
    length = self.paged.models_length
    if selected == 0:
      selected = length - 1
    else:
      selected -= 1
    self.paged.select(selected)
    embed = await self.paged.build(0)
    await interaction.edit_original_response(embed=embed)
class ConfirmationView(ui.View):
  CHECK = '✅'
  UNCHECK = '❌'
  def __init__(self, loop: asyncio.AbstractEventLoop) -> None:
    super().__init__()
    self.future: asyncio.Future[bool] = loop.create_future()
  def get(self) -> asyncio.Future[bool]:
    return self.future
  async def on_error(self, interaction: Interaction, error: Exception, item: ui.Item) -> None:
    try:
      self.future.set_result(False)
    except asyncio.InvalidStateError:
      pass
    return await super().on_error(interaction, error, item)
  async def on_timeout(self):
    try:
      self.future.set_result(False)
    except asyncio.InvalidStateError:
      pass
  @ui.button(emoji=CHECK, custom_id="check")
  async def check(self, interaction: Interaction, btn: ui.Button) -> None:
    await interaction.response.defer()
    self.future.set_result(True)
    self.clear_items()
    self.stop()
  @ui.button(emoji=UNCHECK, custom_id="uncheck")
  async def uncheck(self, interaction: Interaction, btn: ui.Button) -> None:
    await interaction.response.defer()
    self.future.set_result(False)
    self.clear_items()
    self.stop()