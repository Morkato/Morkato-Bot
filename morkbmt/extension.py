from discord.ext.commands.core import (get_signature_parameters, unwrap_function)
from discord.interactions import Interaction
from discord.ext.commands import Command
from discord import app_commands as apc
from .msgbuilder import MessageBuilder
from .context import MorkatoContext
from .types import Coro
from typing_extensions import Self
from typing import (
  get_args,
  get_origin,
  Concatenate,
  ParamSpec,
  Protocol,
  Coroutine,
  ClassVar,
  Generic,
  Optional,
  Callable,
  TypeVar,
  Tuple,
  Union,
  Type,
  List,
  Dict,
  Any
)
import asyncio
import inspect

T = TypeVar('T')
P = ParamSpec('P')
ExceptionT = TypeVar('ExteptionT', bound="Exception")
ExtensionT = TypeVar('ExtensionT', bound="Extension")
GenericCoroCallable = Callable[..., Coro[T]]
ErrorCallbackHandler = Callable[["Extension", "MorkatoContext", ExceptionT], Coro[None]]

class MorkatoCommand(Command[None, P, Any]):
  def __init__(self, func: Callable[Concatenate[MorkatoContext, P], Coro[None]], **kwargs) -> None:
    super().__init__(func, **kwargs)
    self.extension: Optional[Extension] = None
    self._cog = None
  @property
  def cog(self) -> None:
    return None
  @property
  def callback(self) -> Callable[Concatenate[MorkatoContext, P], Coro[None]]:
    return self._callback
  @callback.setter
  def callback(self, func: Callable[Concatenate[MorkatoContext, P], Coro[None]]) -> None:
    self._callback = func
    unwrap = unwrap_function(func)
    self.module: str = unwrap.__module__
    try:
        globalns = unwrap.__globals__
    except AttributeError:
        globalns = {}
    self.params: Dict[str, inspect.Parameter] = get_signature_parameters(func, globalns, skip_parameters=1)
class ErrorCallback(Generic[ExceptionT]):
  def __init__(self, callback: ErrorCallbackHandler[ExceptionT], error_cls: Any) -> None:
    self._extension: Optional[Extension] = None
    self.callback = callback
    self.err_cls = error_cls
  def __call__(self, ctx: MorkatoContext, error: ExceptionT) -> Coro[None]:
    return self.invoke(ctx, error)
  @property
  def extension_name(self) -> str:
    if self._extension is None:
      raise RuntimeError
    return self._extension.__extension_name__
  async def invoke(self, ctx: MorkatoContext, error: ExceptionT) -> None:
    if self._extension is None:
      raise RuntimeError
    await self.callback(ctx, error)
  def set_extension(self, extension: "Extension") -> None:
    self._extension = extension

CommandDecorator = Callable[[GenericCoroCallable[Any]], MorkatoCommand]
ExceptionDecorator = Callable[[ErrorCallbackHandler[ExceptionT]], ErrorCallback[ExceptionT]]
def command(name: str, **attrs) -> CommandDecorator:
  def decorator(func: Callable[..., Coroutine[Any, Any, Any]]) -> MorkatoCommand:
    if isinstance(func, MorkatoCommand):
      raise TypeError
    return MorkatoCommand(func, name=name, **attrs)
  return decorator
def exception(cls: Type[ExceptionT]) -> ExceptionDecorator[ExceptionT]:
  def decorator(func: Callable[[Extension, MorkatoContext, ExceptionT], Coro[None]]) -> ErrorCallback[ExceptionT]:
    return ErrorCallback(func, cls)
  return decorator

class ConverterHandlerMeta(type):
  __converter_name__: str
  __registry_class__: bool
  __inject_values__: Dict[str, Type[Any]]
  def __new__(cls, name: str, bases: Tuple[Any], attrs: Dict[str, Any], /, **kwargs) -> Self:
    inject_values: Dict[str, Type[Any]] = {}
    annotations = attrs.get("__annotations__", {})
    attrs["__converter_name__"] = kwargs.pop("name", name)
    attrs["__registry_class__"] = False
    attrs["__inject_values__"] = inject_values
    if kwargs:
      raise NotImplementedError
    metas = (meta for meta in bases if isinstance(meta, cls))
    for meta in metas:
      inject_values.update(meta.__inject_values__)
    for (key, annotation) in annotations.items():
      if get_origin(annotation) is ClassVar or key.startswith("__") and key.endswith("__"):
        continue
      if isinstance(get_origin(annotation) or annotation, ConverterHandlerMeta):
        raise TypeError("You don't inject converter in anhoter converter.")
      if key in attrs:
        raise ValueError("Value already initialized in namespace.")
      inject_values[key] = annotation
    return super().__new__(cls, name, bases, attrs, **kwargs)
class Converter(Generic[T], metaclass=ConverterHandlerMeta):
  __converter_name__: str
  __registry_class__: bool
  __convert_class__: Type[T]
  __inject_values__: Dict[str, Type[Any]]
  def __init_subclass__(cls, **kwgs) -> None:
    super().__init_subclass__(**kwgs)
    cls.__convert_class__ = get_args(cls.__orig_bases__[0])[0]
  def __init__(self) -> None: ...
  async def convert(self, arg: str, /, **kwargs) -> T:
    raise NotImplementedError
  async def __call__(self, arg: str, /, **kwargs) -> T:
    return await self.convert(arg, **kwargs)
  async def start(self) -> None: ...
  async def setup(self) -> None: ...
  async def close(self) -> None: ...
class ExtensionMeta(type):
  __extension_name__: str
  __inject_values__: Dict[str, Type[Any]]
  def __new__(cls, name: str, bases: List[type], attrs: Dict[str, Any], /, **kwargs) -> Self:
    app_commands: Dict[str, apc.Command[None, ..., Any]] = {}
    commands: Dict[str, Command[Any, ..., Any]] = {}
    handlers: Dict[Type[Any], ErrorCallback] = {}
    inject_values: Dict[str, Type[Any]] = {}
    annotations = attrs.get("__annotations__", {})
    attrs["__extension_name__"] = kwargs.pop("name", name)
    attrs["__extension_app_commands__"] = app_commands
    attrs["__extension_commands__"] = commands
    attrs["__errors_handlers__"] = handlers
    attrs["__inject_values__"] = inject_values
    if kwargs:
      raise NotImplementedError
    metas = (meta for meta in bases if isinstance(meta, cls))
    for meta in metas:
      inject_values.update(meta.__inject_values__)
    for (key, annotation) in annotations.items():
      if get_origin(annotation) is ClassVar or key.startswith("__") and key.endswith("__"):
        continue
      if isinstance(annotation, ExtensionMeta):
        raise TypeError("You don't inject extension in anhoter extension.")
      if key in attrs:
        raise ValueError("Value already initialized in namespace.")
      inject_values[key] = annotation
    for (elem, value) in attrs.items():
      if isinstance(value, MorkatoCommand):
        commands[elem] = value
      elif isinstance(value, apc.Command):
        app_commands[value.name] = value
      elif isinstance(value, ErrorCallback):
        handlers[value.err_cls] = value
    return super().__new__(cls, name, bases, attrs)
class Extension(metaclass=ExtensionMeta):
  __extension_name__: str
  __inject_values__: Dict[str, Type[Any]]
  msgbuilder: MessageBuilder
  def __init__(self) -> None: ...
  async def setup(self, commands: "ExtensionCommandBuilder[Self]") -> None:
    pass
  async def close(self) -> None:
    pass
class ExtensionCommandBuilder(Protocol[ExtensionT]):
  def command(self, name: str, callback: Callable[Concatenate[MorkatoContext, P], Coro[None]], /, **attrs) -> MorkatoCommand[P]: ...
  def app_command(self, name: str, callback: apc.commands.CommandCallback, /, **attrs) -> apc.Command: ...
  def exception(self, cls: Type[ExceptionT], callback: ErrorCallbackHandler[ExceptionT], /) -> ErrorCallback[ExceptionT]: ...
  def check(self, command: Union[MorkatoCommand, apc.Command], predicate: Callable[[MorkatoContext], Union[Coro[bool], bool]]) -> None: ...
  def guild_only(self, command: Union[MorkatoCommand, apc.Command], /) -> None: ...
  def rename(self, command: apc.Command, /, **parameters) -> None: ...
class ExtensionCommandBuilderImpl(ExtensionCommandBuilder[ExtensionT]):
  def __init__(self, extension: ExtensionT):
    self.__extension = extension
    self.__app_commands: Dict[str, apc.Command[None, ..., Any]] = {}
    self.__commands: Dict[str, MorkatoCommand] = {}
    self.__error_handlers: Dict[Type[Any], ErrorCallback[Any]] = {}
  def get_extension(self) -> ExtensionT:
    return self.__extension
  def get_app_commands(self) -> Dict[str, apc.Command[None, ..., Any]]:
    return self.__app_commands
  def get_commands(self) -> Dict[str, MorkatoCommand]:
    return self.__commands
  def get_error_handlers(self) -> Dict[Type[Any], ErrorCallback[Any]]:
    return self.__error_handlers
  def command(self, name: str, callback: Callable[Concatenate[MorkatoContext, P], Coro[None]], /, **attrs) -> MorkatoCommand[P]:
    command = MorkatoCommand(callback, name=name, **attrs)
    command.extension = self.__extension
    self.__commands[name] = command
    return command
  def app_command(self, name: str, callback: apc.commands.CommandCallback, /, **attrs) -> apc.Command:
    register = apc.command(name=name, **attrs)
    command = register(callback)
    self.__app_commands[name] = command
    return command
  def exception(self, cls: Type[ExceptionT], callback: ErrorCallbackHandler[ExceptionT], /) -> ErrorCallback[ExceptionT]:
    handler = ErrorCallback(callback, cls)
    self.__error_handlers[cls] = handler
    handler.set_extension(self.__extension)
    return handler
  def check(self, command: Union[MorkatoCommand, apc.Command], predicate: Callable[[MorkatoContext], Union[Coro[bool], bool]]) -> None:
    checker: Callable[[Union[MorkatoContext, Interaction]]] = predicate
    if isinstance(command, apc.Command):
      async def predicate_interaction(interaction: Interaction[Any]):
        context = await MorkatoContext.from_interaction(interaction)
        if not asyncio.iscoroutinefunction(predicate):
          return predicate(context)
        return await predicate(context)
      checker = predicate_interaction
    command.add_check(checker)
  def guild_only(self, command: Union[MorkatoCommand, apc.Command], /) -> None:
    if isinstance(command, apc.Command):
      register = apc.guild_only()
      register(command)
      return
    checker = lambda ctx: ctx.guild is not None
    self.check(command, checker)
  def rename(self, command: apc.Command, /, **parameters) -> None:
    if isinstance(command, MorkatoCommand):
      return None
    register = apc.rename(**parameters)
    register(command)