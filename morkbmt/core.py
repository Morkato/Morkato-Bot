from __future__ import annotations
from .extension import (ErrorCallback, Converter, Extension, ExtensionCommandBuilderImpl)
from .msgbuilder import MessageBuilder
from discord.interactions import Interaction
from discord.flags import Intents
from discord import app_commands as apc
from glob import glob
from typing import (
  TYPE_CHECKING,
  get_origin,
  get_args,
  overload,
  Optional,
  Iterable,
  TypeVar,
  Type,  
  Dict,
  List,
  Any
)
if TYPE_CHECKING:
  from .types import ToRegistryObject
  from .bot import MorkatoBot
import importlib.util
import inspect
import logging
import traceback
import sys
import os

ToRegistryObjectT = TypeVar('ToRegistryObjectT', bound="ToRegistryObject")
MorkatoBotT = TypeVar("MorkatoBotT", bound="MorkatoBot")
T = TypeVar('T')
_log = logging.getLogger(__name__)

def registry(object: ToRegistryObjectT) -> ToRegistryObjectT:
  object.__registry_class__ = True
  return object
class BotBuilder:
  def __init__(self, msgbuilder: MessageBuilder, home: str, intents: Intents) -> None:
    self.__loaded_converters: Dict[Type[Any], Converter[Any]] = {}
    self.__loaded_extensions: Dict[str, Extension] = {}
    self.__unloaded_extensions: List[Type[Extension]] = []
    self.__unloaded_converters: List[Type[Converter[Any]]] = []
    self.__injected: Dict[Type[Any], Any] = {}
    self.__tree_cls: Optional[Type[apc.CommandTree]] = None
    self.__command_prefix = '!'
    self.__msgbuilder = msgbuilder
    self.__catching: Dict[Type[Any], ErrorCallback] = {}
    self.__home = os.path.abspath(os.path.normpath(home))
    self.__intents = intents
  def to_inject_value(self, annotation: Any) -> Any:
    if annotation is MessageBuilder:
      return self.__msgbuilder
    value = self.__injected.get(annotation)
    if value is None:
      raise TypeError("Annotation: %s.%s is not injected" % (annotation.__module__, annotation.__name__))
    return value
  def command_prefix(self, prefix: str, /) -> None:
    self.__command_prefix = prefix
  def tree(self, cls: Type[apc.CommandTree], /) -> None:
    self.__tree_cls = cls
  def inject(self, cls: Type[T], object: T, /) -> None:
    self.__injected[cls] = object
  def get_unloaded_registries(self, name: str, /, extensions: List[Type[Extension]], converters: List[Type[Converter[Any]]]) -> None:
    if name.endswith(".__init__"):
      name = name[:-9]
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
    registries = (member for (name, member) in members if getattr(member, '__registry_class__', False))
    for registry_class in registries:
      if issubclass(registry_class, Extension):
        extensions.append(registry_class)
      elif issubclass(registry_class, Converter):
        converters.append(registry_class)
  def prepare(self) -> None:
    if not self.__home in sys.path:
      sys.path.append(self.__home)
    unloaded_extensions: Iterable[str] = glob(os.path.join("extension", "*.py"), root_dir=self.__home)
    unloaded_extensions = (uex[:-3].replace('/', '.') for uex in unloaded_extensions)
    for name in unloaded_extensions:
      self.get_unloaded_registries(name, self.__unloaded_extensions, self.__unloaded_converters)
  async def load_converter(self, converter: Type[Converter[Any]], /) -> None:
    values = converter.__inject_values__
    loaded_converter = converter()
    for (key, cls) in values.items():
      try:
        value: Any = self.to_inject_value(cls)
      except TypeError:
        _log.warning("Failed to load converter: %s.%s value: %s (%s.%s) is not injected." % (converter.__module__, converter.__name__, key, cls.__module__, cls.__name__))
        return
      setattr(loaded_converter, key, value)
    self.__loaded_converters[converter.__convert_class__] = loaded_converter
    await loaded_converter.start()
    _log.info("Success to load converter: %s.%s %s values is injected." % (converter.__module__, converter.__name__, len(values)))
  async def load_extension(self, extension: Type[Extension], /) -> Optional[ExtensionCommandBuilderImpl[Extension]]:
    values = extension.__inject_values__
    loaded_extension = extension()
    for (key, cls) in values.items():
      value: Any = None
      try:
        if get_origin(cls) is Converter:
          map_key = get_args(cls)[0]
          value = self.__loaded_converters[map_key]
        else:
          value = self.to_inject_value(cls)
      except TypeError:
        _log.warning("Failed to load extension: %s.%s value: %s (%s.%s) is not injected." % (extension.__module__, extension.__name__, key, cls.__module__, cls.__name__))
        return None
      except KeyError:
        origin = get_args(cls)[0]
        _log.warning("Failed to load extension: %s.%s converter: %s (%s.%s[%s.%s]) is not injected." % (extension.__module__, extension.__name__, key, Converter.__module__, cls.__name__, origin.__module__, origin.__name__))
        return None
      if value is None:
        raise NotImplementedError
      setattr(loaded_extension, key, value)
    commands: ExtensionCommandBuilderImpl[Extension] = ExtensionCommandBuilderImpl(loaded_extension)
    try:
      await loaded_extension.setup(commands)
    except Exception as exc:
      _log.error("Failed to setup extension: %s.%s traceback:", extension.__module__, extension.__name__)
      traceback.print_exc()
      return None
    self.__loaded_extensions[extension.__extension_name__] = loaded_extension
    _log.info("Success to load extension: %s.%s %s values injected." % (extension.__module__, extension.__name__, len(values)))
    return commands
  @overload
  def login(self, cls: Type[MorkatoBotT], /) -> MorkatoBotT: ...
  @overload
  def login(self, /) -> MorkatoBot: ...
  def login(self, cls: Optional[Type[MorkatoBotT]] = None) -> MorkatoBotT:
    if cls is None:
      cls = MorkatoBot
    bot = cls(
      command_prefix=self.__command_prefix,
      tree_cls=self.__tree_cls,
      extensions=self.__loaded_extensions,
      converters=self.__loaded_converters,
      msgbuilder=self.__msgbuilder,
      injected=self.__injected,
      catching=self.__catching,
      intents=self.__intents
    )
    return bot
  async def setup(self, bot: MorkatoBot) -> None:
    for unloaded_converter in self.__unloaded_converters:
      await self.load_converter(unloaded_converter)
    for unloaded_extension in self.__unloaded_extensions:
      commands = await self.load_extension(unloaded_extension)
      if commands is None:
        continue
      for command in commands.get_commands().values():
        bot.add_command(command)
      for app_command in commands.get_app_commands().values():
        bot.tree.add_command(app_command)
      self.__catching.update(commands.get_error_handlers())
class MorkatoCommandTree(apc.CommandTree[MorkatoBotT]):
  async def on_error(self, interaction: Interaction[MorkatoBotT], exception: apc.AppCommandError):
    ctx = await interaction.client.get_context(interaction)
    base_exception: Optional[Exception] = None
    if isinstance(exception, apc.CommandInvokeError):
      base_exception = exception.original
    exc_cls = type(exception)
    callback = interaction.client.morkcatching.get(exc_cls)
    if callback is not None:
      await callback.invoke(ctx, exception)
      return
    if base_exception is None:
      return await super().on_error(interaction, exception)
    base_exc_cls = type(base_exception)
    callback = interaction.client.morkcatching.get(base_exc_cls)
    if callback is None:
      try:
        catching = (callback for (cls, callback) in interaction.client.morkcatching.items() if issubclass(base_exc_cls, cls))
        callback = next(catching)
      except StopIteration:
        return await super().on_error(interaction, exception)
    await callback.invoke(ctx, base_exception)