from __future__ import annotations
from .extension import (Extension, ErrorCallback, get_extensions)
from discord.ext.commands.errors import CommandError
from morkato.state import MorkatoConnectionState
from morkato.utils import parse_arguments
from discord.ext.commands.bot import Bot
from discord.message import Message
from .context import MorkatoContext
from morkato.http import HTTPClient
from types import MethodType
from typing_extensions import Self
from typing import (
  Iterable,
  TypeVar,
  Type,  
  Dict,
  Any
)
import inspect
import logging

ExtensionT = TypeVar('ExtensionT', bound=Extension)
_log = logging.getLogger(__name__)
class ExtensionManager:
  def __init__(self, bot: MorkatoBot) -> None:
    self.loaded_extensions: Dict[str, Extension] = {}
    self.catching: Dict[Type[Any], ErrorCallback] = {}
    self.bot = bot
  def _get_value(self, annotation: Any) -> Any:
    if annotation is MorkatoConnectionState:
      return self.bot.morkato_connection
    elif annotation is HTTPClient:
      return self.bot.morkato_http
    raise TypeError
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
      self.bot.add_command(command)
      command._callback = MethodType(command._callback, loaded_extension)
      command._extension = extension
    for command in extension.__extension_app_commands__.copy().values():
      self.bot.tree.add_command(command)
      command._callback = MethodType(command._callback, loaded_extension)
    for handler in extension.__errors_handlers__.copy().values():
      self.catching[handler.err_cls] = handler
      handler.set_extension(loaded_extension)
  async def unload_extension(self, name: str) -> None:
    extension = self.loaded_extensions.pop(name)
    await extension.close()
    for command_name in extension.__extension_commands__.keys():
      self.bot.remove_command(command_name)
    for command_name in extension.__extension_app_commands__.keys():
      self.bot.tree.remove_command(command_name)
    for handler in extension.__errors_handlers__.keys():
      self.catching.pop(handler, None)
    if extension.__extension_app_commands__:
      await self.bot.tree.sync()
class MorkatoBot(Bot):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.extension_manager = ExtensionManager(self)
    self.morkato_http: HTTPClient = HTTPClient(self.loop)
    self.morkato_connection: MorkatoConnectionState = MorkatoConnectionState(self.dispatch, http=self.morkato_http)
  async def __aenter__(self) -> Self:
    await super().__aenter__()
    await self.morkato_http.static_login()
    return self
  async def __aexit__(self, *args) -> None:
    await super().__aexit__(*args)
    await self.morkato_http.close()
  async def _async_setup_hook(self) -> None:
    await super()._async_setup_hook()
    self.morkato_http.loop = self.loop
  async def get_context(self, message: Message, /) -> MorkatoContext:
    ctx = await super().get_context(message, cls=MorkatoContext)
    if ctx.guild is not None:
      morkato_guild = self.morkato_connection.get_cached_guild(ctx.guild.id)
      if morkato_guild is None:
        morkato_guild = self.morkato_connection.create_guild(ctx.guild.id)
      ctx.morkato_guild = morkato_guild
    return ctx
  async def on_ready(self) -> None:
    await self.tree.sync()
    _log.info("Estou conectado, como: %s" % self.user.name)
  def dispatch(self, event_name: str, /, *args: Any, **kwargs: Any) -> None:
    super().dispatch(event_name, *args, **kwargs)
    for extension in self.extension_manager.values():
      listeners = extension.__extension_listeners__.get(event_name, [])
      for listener in listeners:
        self._schedule_event(listener, event_name, extension, *args, **kwargs)
  async def setup_hook(self) -> None:
    for cls in get_extensions().values():
      await self.extension_manager.load_extension(cls)
  async def on_command_error(self, context: MorkatoContext, exception: CommandError) -> None:
    try:
      exc_cls = type(exception)
      callback = self.extension_manager.catching[exc_cls]
    except KeyError:
      return await super().on_command_error(context, exception)
    await callback.invoke(context, exception)  