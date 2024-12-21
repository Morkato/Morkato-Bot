from __future__ import annotations
from .extension import (ErrorCallback, Converter, Extension, ExtensionCommandBuilderImpl, ApplicationContextImpl)
from .errors import (ValueNotInjectedError, ConverterNotInjectedError, ExtensionInvokeError, ConverterInvokeError)
from .msgbuilder import MessageBuilder
from discord.ext.commands import CommandRegistrationError
from discord.interactions import Interaction
from discord.flags import Intents
from discord import app_commands as apc
from glob import glob
from typing import (
  TYPE_CHECKING,
  Callable,
  get_origin,
  get_args,
  overload,
  Optional,
  Iterable,
  TypeVar,
  Union,
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
def _get_unloaded_registries(name: str, /, extensions: List[Type[Extension]], converters: List[Type[Converter[Any]]]) -> None:
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
def _inject_in_converter(converter: Converter[Any], *, injector: Callable[[Any], Optional[Any]]) -> int:
  values = converter.__inject_values__
  for (key, cls) in values.items():
    is_optional = False
    map_cls = cls
    if get_origin(map_cls) is Union:
      args = get_args(cls)
      is_optional = True
      map_cls = get_args(cls)[0]
    value = injector(map_cls)
    if value is None and not is_optional:
      raise ValueNotInjectedError(key, cls)
    setattr(converter, key, value)
  return len(values)
def _inject_in_extension(extension: Extension, *, converters: Dict[Type[Any], Converter[Any]], injector: Callable[[Any], Optional[Any]]) -> int:
  values = extension.__inject_values__
  for (key, cls) in values.items():
    is_optional = False
    map_cls = cls
    value: Any
    if get_origin(map_cls) is Union:
      is_optional = True
      map_cls = get_args(cls)[0]
    if get_origin(map_cls) is Converter:
      conv_key = get_args(cls)[0]
      value = converters.get(conv_key)
    else:
      value = injector(map_cls)
    if value is None and not is_optional:
      if get_origin(cls) is Converter:
        raise ConverterNotInjectedError(key, get_args(cls)[0])
      raise ValueNotInjectedError(key, cls)
    setattr(extension, key, value)
  return len(values)
def _load_commands(bot: MorkatoBot, commands: ExtensionCommandBuilderImpl) -> None:
  try:
    for command in commands.get_commands().values():
      bot.add_command(command)
    for app_command in commands.get_app_commands().values():
      bot.tree.add_command(app_command)
    bot.morkcatching.update(commands.get_error_handlers())
  except (apc.CommandAlreadyRegistered, CommandRegistrationError) as exc:
    for app_command in commands.get_app_commands().keys():
      bot.tree.remove_command(app_command)
    for command in commands.get_commands().keys():
      bot.remove_command(command)
    raise exc
class BotBuilder:
  def __init__(self, msgbuilder: MessageBuilder, home: str, intents: Intents) -> None:
    self.__unloaded_extensions: Dict[str, Extension] = {}
    self.__unloaded_converters: Dict[Type[Any], Converter[Any]] = {}
    self.__injected: Dict[Type[Any], Any] = {}
    self.__tree_cls: Optional[Type[apc.CommandTree]] = None
    self.__command_prefix = '!'
    self.__msgbuilder = msgbuilder
    self.__catching: Dict[Type[Any], ErrorCallback] = {}
    self.__home = os.path.abspath(os.path.normpath(home))
    self.__intents = intents
    self.__prepared = False
  def get_injected_value(self, annotation: Any) -> Optional[Any]:
    if annotation is MessageBuilder:
      return self.__msgbuilder
    return self.__injected.get(annotation)
  def get_all_extensions(self) -> Dict[str, Extension]:
    return self.__unloaded_extensions.copy()
  def get_all_converters(self) -> Dict[Type[Any], Converter[Any]]:
    return self.__unloaded_converters.copy()
  def command_prefix(self, prefix: str, /) -> None:
    self.__command_prefix = prefix
  def tree(self, cls: Type[apc.CommandTree], /) -> None:
    self.__tree_cls = cls
  def inject(self, object: Any, /) -> None:
    self.__injected[type(object)] = object
  def prepare(self) -> None:
    if self.__prepared:
      return
    if not self.__home in sys.path:
      sys.path.append(self.__home)
    unloaded_extensions_path: Iterable[str] = glob(os.path.join("extension", "*.py"), root_dir=self.__home)
    unloaded_extensions_path = (uex[:-3].replace('/', '.') for uex in unloaded_extensions_path)
    unloaded_converters: List[Type[Converter[Any]]] = []
    unloaded_extensions: List[Type[Extension]] = []
    for name in unloaded_extensions_path:
      _get_unloaded_registries(name, unloaded_extensions, unloaded_converters)
    for converter in unloaded_converters:
      self.registry_converter(converter)
    for extension in unloaded_extensions:
      self.registry_extension(extension)
    self.__prepared = True
  def registry_converter(self, converter: Type[Converter[T]], /) -> Converter[T]:
    unloaded_converter: Converter[T]
    try:
      unloaded_converter = converter()
      unloaded_converter.start()
    except Exception as exc:
      _log.warning("Failed to start converter: %s.%s error is called:\n%s", converter.__module__, converter.__name__, traceback.format_exc())
      return
    self.__unloaded_converters[converter.__convert_class__] = unloaded_converter
    return unloaded_converter
  def registry_extension(self, extension: Type[Extension], /) -> Extension:
    unloaded_extension: Extension
    try:
      unloaded_extension = extension()
      application = ApplicationContextImpl(extension, self.__injected)
      unloaded_extension.start(application)
    except Exception as exc:
      _log.warning("Failed to start extension: %s.%s error is called:\n%s", extension.__module__, extension.__name__, traceback.format_exc())
      return
    self.__unloaded_extensions[extension.__extension_name__] = unloaded_extension
    return unloaded_extension
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
      msgbuilder=self.__msgbuilder,
      injected=self.__injected,
      catching=self.__catching,
      intents=self.__intents
    )
    return bot
  async def setup(self, bot: MorkatoBot) -> None:
    copy_converters: Dict[Type[Any], Converter[Any]] = self.get_all_converters()
    copy_extensions: Dict[str, Extension] = self.get_all_extensions()
    for (cls, converter) in copy_converters.items():
      injected: int
      try:
        injected = _inject_in_converter(converter, injector=self.get_injected_value)
        await converter.setup()
      except ValueNotInjectedError as exc:
        _log.error("Failed to load converter: %s.%s(%s[%s.%s]) dependence: %s.%s (%s) is not injected.",
                    converter.__module__, type(converter).__name__, Converter.__name__,
                    converter.__convert_class__.__module__, converter.__convert_class__.__name__,
                    exc.annotation.__module__, exc.annotation.__name__, exc.key)
        continue
      except Exception as exc:
        _log.error("Failed to load converter: %s.%s (%s[%s.%s]) an unexpected error occurred:\n%s",
                   converter.__module__, type(converter).__name__, Converter.__name__,
                   converter.__convert_class__.__module__, converter.__convert_class__.__name__, traceback.format_exc())
        await converter.close()
        continue
      bot.morkconverters[cls] = converter
      _log.info("Success to load converter: %s.%s %s values injected.", converter.__module__, type(converter).__name__, injected)
    for extension in copy_extensions.values():
      injected: int
      try:
        injected = _inject_in_extension(extension, converters=bot.morkconverters, injector=self.get_injected_value)
        commands = ExtensionCommandBuilderImpl(extension)
        await extension.setup(commands)
        _load_commands(bot, commands)
      except ValueNotInjectedError as exc:
        _log.error("Failed to load extension: %s.%s dependence: %s.%s (%s) is not injected.",
                    extension.__module__, type(extension).__name__,
                    exc.annotation.__module__, exc.annotation.__name__,
                    exc.key)
        continue
      except ConverterNotInjectedError as exc:
        _log.error("Failed to load extension: %s.%s converter: %s[%s.%s] (%s) is not injected.",
                    extension.__module__, type(extension).__name__, Converter.__name__,
                    exc.value.__module__, exc.value.__name__, exc.key)
        continue
      except (apc.CommandAlreadyRegistered, CommandRegistrationError) as exc:
        _log.error("Failed to load extension: %s.%s command: %s already registered.",
                    extension.__module__, type(extension).__name__, exc.name)
        await extension.close()
        continue
      except Exception as exc:
        _log.error("Failed to load extension: %s.%s an unexpected error occurred:\n%s",
                   extension.__module__, type(extension).__name__, traceback.format_exc())
        await extension.close()
        continue
      bot.morkextensions[extension.__extension_name__] = extension
      _log.info("Success to load extension: %s.%s %s values injected.", extension.__module__, type(extension).__name__, injected)
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