from __future__ import annotations
from discord.ext.commands.bot import Bot
from discord.ext.commands.errors import (
  CommandError,
  CommandInvokeError,
  ConversionError
)
from .errors import (ExtensionInvokeError, ConverterInvokeError, ValueNotInjectedError)
from .extension import (ErrorCallback, Extension, Converter)
from .core import (MorkatoCommandTree, MessageBuilder)
from .context import MorkatoContext
from typing import (
  get_origin,
  get_args,
  Optional,
  TypeVar,
  Union,
  Type,
  Dict,
  Any
)
import discord.utils
import discord
import logging

_log = logging.getLogger(__name__)
T = TypeVar('T')
class MorkatoBot(Bot):
  def __init__(
    self, *args,
    msgbuilder: MessageBuilder,
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
    self.msgbuilder = msgbuilder
    self.morkextensions: Dict[str, Extension] = {}
    self.morkconverters: Dict[Type[Any], Converter[Any]] = {}
    self.morkcatching = catching
    self.injected = injected
  async def get_context(self, origin: Union[discord.Message, discord.Interaction], /) -> MorkatoContext:
    return await super().get_context(origin, cls=MorkatoContext)
  async def _async_setup_hook(self) -> None:
    await super()._async_setup_hook()
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
  def inject(self, object: Any, /) -> None:
    self.injected[type(object)] = object
  async def close(self) -> None:
    task = self.loop.create_task(super().close(), name="discord.py: Client.close()")
    for extension in self.morkextensions.values():
      await extension.close()
    for converter in self.morkconverters.values():
      await converter.close()
    self.morkextensions.clear()
    self.morkconverters.clear()
    await task
  async def login(self, token: str) -> None:
    await super().login(token)
    self.inject(self.user)