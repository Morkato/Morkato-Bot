from typing import List

from discord import (
  Interaction,
  Embed,

  ui
)

class Embeds(ui.View):
  TIMEOUT: int = 20

  def __init__(self, embeds: List[Embed], *, start: int = 0) -> None:
    super().__init__(timeout=Embeds.TIMEOUT)

    self.idx    = start
    self.length = len(embeds)
    self.embeds = embeds
  
  async def on_timeout(self) -> None:
    self.clear_items()

  @ui.button(
    label='⏪',
    custom_id='rewind'
  )
  async def rewind(self, interaction: Interaction, item: ui.Button) -> None:
    self.idx = self.length - 1 if self.idx == 0 else self.idx - 1

    await interaction.response.edit_message(embed=self.embeds[self.idx])

  @ui.button(
    label='⏩',
    custom_id='forward'
  )
  async def forward(self, interaction: Interaction, item: ui.Button) -> None:
    self.idx = 0 if self.idx + 1 == self.length else self.idx + 1

    await interaction.response.edit_message(embed=self.embeds[self.idx])
