from __future__ import annotations
from discord.ext.commands.bot import Bot
from discord.ext.commands.errors import (
  CommandError,
  CommandInvokeError,
  ConversionError
)
from discord.message import Message
from .tree import MorkatoCommandTree
from .context import MorkatoContext
from .project import ProjectManager
from .extension import Extension
from .converters import Converter
from types import ModuleType
from typing import (
  Optional,
  TypeVar,
  Type,  
  Any
)
import importlib.util
import inspect
import logging
import sys

_log = logging.getLogger(__name__)
T = TypeVar('T')

class MorkatoBot(Bot):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs, tree_cls=MorkatoCommandTree)
    self.project = ProjectManager(
      add_command = self.add_command,
      tree_add_command = self.tree.add_command,
      remove_command = self.remove_command,
      tree_remove_command = self.tree.remove_command,
      tree_sync = self.tree.sync,
      base_message_builder=kwargs.pop("base_message_builder", None)
    )
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
    callback = self.project.catching.get(exc_cls)
    if callback is not None:
      await callback.invoke(context, exception)
      return
    if base_exception is None:
      return await super().on_command_error(context, exception)
    base_exc_cls = type(base_exception)
    callback = self.project.catching.get(base_exc_cls)
    if callback is None:
      try:
        catching = (callback for (cls, callback) in self.project.catching.items() if issubclass(base_exc_cls, cls))
        callback = next(catching)
      except StopIteration:
        return await super().on_command_error(context, exception)
    await callback.invoke(context, base_exception)
  async def load_morkato_extension(self, name: str, /) -> None:
    if name.endswith(".__init__"):
      name = name.strip(".__init__")
    try:
      module = sys.modules[name]
    except KeyError:
      spec = importlib.util.find_spec(name)
      if spec is None:
        raise ModuleNotFoundError("Module is not found: %s" % name)
      module = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(module)
      sys.modules[module.__name__] = module
    members = inspect.getmembers(module)
    to_loaded_members = (member for (name, member) in members if getattr(member, '__registry_class__', False))
    for cls in to_loaded_members:
      if issubclass(cls, Extension):
        await self.project.load_extension(cls)
      if issubclass(cls, Converter):
        await self.project.load_converter(cls)
  def dispatch(self, event_name: str, /, *args: Any, **kwargs: Any) -> None:
    super().dispatch(event_name, *args, **kwargs)
    for extension in self.project.values():
      listeners = extension.__extension_listeners__.get(event_name, [])
      for listener in listeners:
        self._schedule_event(listener, event_name, extension, *args, **kwargs)
  def inject(self, cls: Type[T], object: T, /) -> None:
    self.project.inject(cls, object)