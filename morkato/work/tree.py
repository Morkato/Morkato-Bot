from .context import MorkatoContext
from discord import (
  app_commands as apc,
  Interaction
)
from typing import (
  TYPE_CHECKING,
  Optional,
  Any
)
if TYPE_CHECKING:
  from .bot import MorkatoBot
else:
  MorkatoBot = Any

class MorkatoCommandTree(apc.CommandTree[MorkatoBot]):
  async def handle_error(self, ctx: MorkatoContext, exception: Exception) -> None:
    cls = type(exception)
    handler = self.client.project.get_error_handler(cls)
    await handler.invoke(ctx, exception)
  async def on_error(self, interaction: Interaction, exception: apc.AppCommandError) -> None:
    context = await MorkatoContext.from_interaction(interaction)
    try:      
      if isinstance(exception, (apc.CommandInvokeError)):
        try:
          await self.handle_error(context, exception.original)
          return
        except KeyError:
          pass
      await self.handle_error(context, exception)
    except KeyError:
      super().on_error(interaction, exception)