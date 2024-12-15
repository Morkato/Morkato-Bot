from .command import MorkatoCommand, Command
from .types import ListenerFuncType, Coro
from discord.interactions import Interaction
from discord.ext.commands import Command
from discord import app_commands as apc
from .context import MorkatoContext
from typing_extensions import Self
from typing import (
  get_args,
  Coroutine,
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

ExceptionT = TypeVar('ExteptionT', bound=Exception)
T = TypeVar('T')
def listener(name: str):
  def decorator(func: ListenerFuncType) -> ListenerFuncType:
    func._listener_name = name
    return func
  return decorator
def command(name: str, **attrs):
  def decorator(func: Callable[..., Coroutine[Any, Any, Any]]) -> MorkatoCommand:
    if isinstance(func, MorkatoCommand):
      raise TypeError
    return MorkatoCommand(func, name=name, **attrs)
  return decorator
def exception(cls: Type[Exception]):
  def decorator(func: Callable[[Extension, MorkatoContext, ExceptionT], Coro[None]]) -> ErrorCallback[ExceptionT]:
    return ErrorCallback(func, cls)
  return decorator
class ConverterHandlerMeta(type):
  __converter_name__: str
  __registry_class__: bool
  def __new__(cls, name: str, bases: Tuple[Any], attrs: Dict[str, Any], /, **kwargs) -> Self:
    name = kwargs.pop("name", name)
    attrs["__converter_name__"] = kwargs.pop("name", name)
    attrs["__registry_class__"] = False
    return super().__new__(cls, name, bases, attrs, **kwargs)
class Converter(Generic[T], metaclass=ConverterHandlerMeta):
  __converter_name__: str
  __registry_class__: bool
  __convert_class__: Type[T]
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
class ErrorCallback(Generic[ExceptionT]):
  def __init__(self, callback: Callable[["Extension", MorkatoContext, ExceptionT], Coro[None]], error_cls: Any) -> None:
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
class ExtensionMeta(type):
  __extension_name__: str
  __extension_app_commands__: Dict[str, apc.Command[None, ..., Any]]
  __extension_commands__: Dict[str, Command[Any, ..., Any]]
  __extension_listeners__: Dict[str, List[Callable[..., Coro]]]
  __errors_handlers__: Dict[Type[Any], ErrorCallback]
  def __new__(cls, name: str, bases: List[type], attrs: Dict[str, Any], /, **kwargs) -> Self:
    app_commands: Dict[str, apc.Command[None, ..., Any]] = {}
    commands: Dict[str, Command[Any, ..., Any]] = {}
    listeners: Dict[str, List[ListenerFuncType]] = {}
    handlers: Dict[Type[Any], ErrorCallback] = {}
    to_inject_converters: Dict[str, Type[Any]] = {}
    attrs["__extension_name__"] = kwargs.pop("name", name)
    attrs["__extension_app_commands__"] = app_commands
    attrs["__extension_commands__"] = commands
    attrs["__extension_listeners__"] = listeners
    attrs["__errors_handlers__"] = handlers
    attrs["__to_inject_converters__"] = to_inject_converters
    if kwargs:
      raise NotImplementedError
    for (elem, value) in attrs.items():
      if isinstance(value, MorkatoCommand):
        commands[elem] = value
      elif isinstance(value, apc.Command):
        app_commands[value.name] = value
      elif callable(value):
        if hasattr(value, "_listener_name"):
          name = getattr(value, "_listener_name")
          try:
            listeners[name].append(value)
          except KeyError:
            listeners[name] = [value]
        elif isinstance(value, ErrorCallback):
          handlers[value.err_cls] = value
    return super().__new__(cls, name, bases, attrs)
class Extension(metaclass=ExtensionMeta):
  __extension_name__: str
  __extension_app_commands__: Dict[str, apc.Command[None, ..., Any]]
  __extension_commands__: Dict[str, MorkatoCommand]
  __extension_listeners__: Dict[str, List[Callable[..., Coro]]]
  __errors_handlers__: Dict[Type[Any], ErrorCallback]
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