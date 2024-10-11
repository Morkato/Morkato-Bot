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
  async def on_error(self, interaction: Interaction, exception: apc.AppCommandError) -> None:
    context = await MorkatoContext.from_interaction(interaction)
    extension_manager = self.client.extension_manager
    base_exception: Optional[Exception] = None
    if isinstance(exception, (apc.CommandInvokeError)):
      base_exception = exception.original
    exc_cls = type(exception)
    callback = extension_manager.catching.get(exc_cls)
    if callback is not None:
      await callback.invoke(context, exception)
      return
    if base_exception is None:
      return await super().on_error(interaction, exception)
    base_exc_cls = type(base_exception)
    callback = extension_manager.catching.get(base_exc_cls)
    if callback is None:
      try:
        catching = (callback for (cls, callback) in extension_manager.catching.items() if issubclass(base_exc_cls, cls))
        callback = next(catching)
      except StopIteration:
        return await super().on_error(interaction, exception)
    await callback.invoke(context, base_exception)