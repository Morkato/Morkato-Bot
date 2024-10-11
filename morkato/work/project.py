from morkato.utils import parse_arguments
from .extension import (ErrorCallback, Extension)
from .converters import (ConverterManager, Converter)
from .types import (ToRegistryObject, Coro)
from .builder import MessageBuilder
from discord.ext.commands.core import Command
from discord import app_commands as apc
from types import MethodType
from typing import (
  Optional,
  Callable,
  Iterable,
  TypeVar,
  Type,  
  Dict,
  Any
)
import inspect
import logging

ToRegistryObjectT = TypeVar('ToRegistryObjectT', bound=ToRegistryObject)
ExtensionT = TypeVar('ExtensionT', bound=Extension)
T = TypeVar('T')
_log = logging.getLogger(__name__)

def registry(object: ToRegistryObjectT) -> ToRegistryObjectT:
  object.__registry_class__ = True
  return object
class ProjectManager:
  def __init__(
    self, *,
    add_command: Callable[[Command], None],
    tree_add_command: Callable[[apc.Command], None],
    remove_command: Callable[[str], None],
    tree_remove_command: Callable[[apc.Command], None],
    tree_sync: Callable[..., Coro[None]],
    base_message_builder: Optional[str] = None
  ) -> None:
    self.loaded_extensions: Dict[str, Extension] = {}
    self.converters: ConverterManager = ConverterManager()
    self.catching: Dict[Type[Any], ErrorCallback] = {}
    self.injected: Dict[Type[Any], Any] = {}
    self.builder = MessageBuilder(base_message_builder)
    self.add_command = add_command
    self.tree_add_command = tree_add_command
    self.remove_command = remove_command
    self.tree_remove_command = tree_remove_command
    self.sync = tree_sync
  def _get_value(self, annotation: Any) -> Any:
    if annotation is ConverterManager:
      return self.converters
    elif annotation is MessageBuilder:
      return self.builder
    try:
      return self.injected[annotation]
    except KeyError:
      raise TypeError("Annotation: %s.%s is not injected" % (annotation.__module__, annotation.__name__))
  def inject(self, cls: Type[T], object: T, /) -> None:
    self.injected[cls] = object
  def values(self) -> Iterable[Extension]:
    return self.loaded_extensions.values()
  def add_extension(self, extension: ExtensionT) -> None:
    self.loaded_extensions[extension.__extension_name__] = extension
  async def load_extension(self, extension: Type[ExtensionT], /) -> None:
    parameters = inspect.signature(MethodType(extension.__init__, object())).parameters
    (args, kwargs) = parse_arguments(parameters, key=self._get_value)
    loaded_extension = extension(*args, **kwargs)
    await loaded_extension.setup()
    for command in extension.__extension_commands__.copy().values():
      self.add_command(command)
      command._callback = MethodType(command._callback, loaded_extension)
      command._extension = extension
    for command in extension.__extension_app_commands__.copy().values():
      self.tree_add_command(command)
      command._callback = MethodType(command._callback, loaded_extension)
    for handler in extension.__errors_handlers__.copy().values():
      self.catching[handler.err_cls] = handler
      handler.set_extension(loaded_extension)
    _log.info("Extension: %s.%s is already loaded" % (extension.__module__, extension.__name__))
  async def unload_extension(self, name: str) -> None:
    extension = self.loaded_extensions.pop(name)
    await extension.close()
    for command_name in extension.__extension_commands__.keys():
      self.remove_command(command_name)
    for command_name in extension.__extension_app_commands__.keys():
      self.tree_remove_command(command_name)
    for handler in extension.__errors_handlers__.keys():
      self.catching.pop(handler, None)
    if extension.__extension_app_commands__:
      await self.sync()
  async def load_converter(self, converter: Type[Converter[Any, Any]], /) -> None:
    parameters = inspect.signature(MethodType(converter.__init__, object())).parameters
    (args, kwargs) = parse_arguments(parameters, key=self._get_value)
    loaded_converter = converter(*args, **kwargs)
    await loaded_converter.setup()
    self.converters.loaded[converter] = loaded_converter
    _log.info("Converter: %s.%s is already loaded" % (converter.__module__.strip(".__init__"), converter.__name__))
  async def unload_converter(self, converter: Type[Converter[Any, Any]], /) -> None:
    try:
      loaded_converter = self.converters.loaded.pop(converter)
      await loaded_converter.close()
    except KeyError:
      pass