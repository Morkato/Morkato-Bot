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

T = TypeVar('T')
ExceptionT = TypeVar('ExteptionT', bound="Exception")
GenericCoroCallable = Callable[..., Coro[T]]
ErrorCallbackHandler = Callable[["Extension", "MorkatoContext", ExceptionT], Coro[None]]

class MorkatoCommand(Command[None, ..., Any]):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.extension: Optional[Extension] = None
  @property
  def cog(self) -> None:
    return None
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
    await self.callback(self._extension, ctx, error)
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
  __extension_app_commands__: Dict[str, apc.Command[None, ..., Any]]
  __extension_commands__: Dict[str, Command[Any, ..., Any]]
  __errors_handlers__: Dict[Type[Any], ErrorCallback]
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
  __extension_app_commands__: Dict[str, apc.Command[None, ..., Any]]
  __extension_commands__: Dict[str, MorkatoCommand]
  __errors_handlers__: Dict[Type[Any], ErrorCallback]
  __inject_values__: Dict[str, Type[Any]]
  msgbuilder: MessageBuilder
  def __init__(self) -> None: ...
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
  async def start(self) -> None:
    pass
  async def setup(self) -> None:
    pass
  async def close(self) -> None:
    pass