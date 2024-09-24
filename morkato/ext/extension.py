from morkato.state import MorkatoConnectionState
from discord.interactions import Interaction
from .command import MorkatoCommand, Command
from .types import ListenerFuncType, Coro
from discord.ext.commands import Command
from discord import app_commands as apc
from .context import MorkatoContext
from morkato.http import HTTPClient
from typing_extensions import Self
from morkato.abc import Snowflake
from morkato.guild import Guild
from discord import ui
from typing import (
  Coroutine,
  Optional,
  Callable,
  Type,
  List,
  Dict,
  Any
)

__all_extensions__: Dict[str, "Extension"] = {}
def get_extensions() -> Dict[str, "Extension"]:
  return  __all_extensions__
def extension(cls):
  if not issubclass(cls, Extension):
    raise TypeError("This: %s is not an Extension" % cls.__name__)
  __all_extensions__[cls.__extension_name__] = cls
  return cls
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
  def decorator(func: Callable[[Extension, MorkatoContext, Exception], Coro[None]]) -> ErrorCallback:
    return ErrorCallback(func, cls)
  return decorator
class ErrorCallback:
  def __init__(self, callback: Callable[["Extension", MorkatoContext, Exception], Coro[None]], error_cls: Any) -> None:
    self._extension: Optional[Extension] = None
    self.callback = callback
    self.err_cls = error_cls
  def __call__(self, ctx: MorkatoContext, error: Exception) -> Coro[None]:
    return self.invoke(ctx, error)
  @property
  def extension_name(self) -> str:
    if self._extension is None:
      raise RuntimeError
    return self._extension.__extension_name__
  async def invoke(self, ctx: MorkatoContext, error: Exception) -> None:
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
    attrs["__extension_name__"] = kwargs.pop("name", name)
    attrs["__extension_app_commands__"] = app_commands
    attrs["__extension_commands__"] = commands
    attrs["__extension_listeners__"] = listeners
    attrs["__errors_handlers__"] = handlers
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
  __extension_commands__: Dict[str, Command[Any, ..., Any]]
  __extension_listeners__: Dict[str, List[Callable[..., Coro]]]
  __errors_handlers__: Dict[Type[Any], ErrorCallback]
  async def setup(self) -> None:
    pass
  async def close(self) -> None:
    pass
class ApplicationExtension(Extension):
  def __init__(self, connection: MorkatoConnectionState, http: HTTPClient) -> None:
    self.connection = connection
    self.http = http
  async def get_morkato_guild(self, guild: Snowflake) -> Guild:
    morkato = self.connection.get_cached_guild(guild.id)
    if morkato is None:
      morkato = self.connection.create_guild(guild.id)
    return morkato
  async def send_confirmation(self, interaction: Interaction, **options) -> bool:
    view = ConfirmationView()
    if interaction.response.is_done():
      await interaction.edit_original_response(view=view, **options)
    else:
      await interaction.response.send_message(view=view, **options)
    return await view.get_value()
class ConfirmationView(ui.View):
  CHECK = '✅'
  UNCHECK = '❌'
  def __init__(self) -> None:
    super().__init__(timeout=20)
    self.confirmed = False
  async def get_value(self) -> bool:
    await self.wait()
    return self.confirmed
  @ui.button(emoji=CHECK, custom_id="check")
  async def check(self, interaction: Interaction, btn: ui.Button) -> None:
    await interaction.response.defer()
    self.confirmed = True
    self.stop()
  @ui.button(emoji=UNCHECK, custom_id="uncheck")
  async def uncheck(self, interaction: Interaction, btn: ui.Button) -> None:
    await interaction.response.defer()
    self.stop()