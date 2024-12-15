from __future__ import annotations
from discord.ext.commands.core import GroupMixin
from discord.ext.commands.bot import Bot
from discord.ext.commands.errors import (
  CommandError,
  CommandInvokeError,
  ConversionError
)
from .extension import (ErrorCallback, Extension, Converter)
from discord.message import Message
from .tree import MorkatoCommandTree
from .context import MorkatoContext
from .builder import MessageBuilder
from typing import (
  Optional,
  TypeVar,
  Type,
  Dict,
  Any
)
import logging

_log = logging.getLogger(__name__)
T = TypeVar('T')
class MorkatoBot(Bot):
  def __init__(
    self, *args,
    content: MessageBuilder,
    extensions: Dict[str, Extension],
    converters: Dict[Type[Any], Converter[Any]],
    catching: Dict[Type[Any], ErrorCallback],
    injected: Dict[Type[Any], Any],
    **kwargs
  ) -> None:
    tree_cls = kwargs.pop("tree_cls", None)
    if tree_cls is None:
      tree_cls = MorkatoCommandTree
    super().__init__(
      *args,
      **kwargs,
      tree_cls=tree_cls
    )
    self.morkcontent = content
    self.morkextensions = extensions
    self.morkconverters = converters
    self.morkcatching = catching
    self.injected = injected
  async def get_context(self, message: Message, /) -> MorkatoContext:
    return await super().get_context(message, cls=MorkatoContext)
  async def on_ready(self) -> None:
    await self.tree.sync()
    _log.info("Estou conectado, como: %s" % self.user.name)
  async def on_command_error(self, context: MorkatoContext, exception: CommandError) -> None:
    base_exception: Optional[Exception] = None
    if isinstance(exception, (CommandInvokeError, ConversionError)):
      base_exception = exception.original
    exc_cls = type(exception)
    callback = self.morkcatching.get(exc_cls)
    if callback is not None:
      await callback.invoke(context, exception)
      return
    if base_exception is None:
      return await super().on_command_error(context, exception)
    base_exc_cls = type(base_exception)
    callback = self.morkcatching.get(base_exc_cls)
    if callback is None:
      try:
        catching = (callback for (cls, callback) in self.morkcatching.items() if issubclass(base_exc_cls, cls))
        callback = next(catching)
      except StopIteration:
        return await super().on_command_error(context, exception)
    await callback.invoke(context, base_exception)
  def inject(self, cls: Type[T], object: T, /) -> None:
    self.injected[cls] = object