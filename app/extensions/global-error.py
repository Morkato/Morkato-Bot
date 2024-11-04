from morkato.work.builder import UnknownMessageContent
from morkato.work.context import MorkatoContext
from morkato.work.extension import exception
from morkato.work.project import registry
from app.extension import BaseExtension
from app.errors import (AppError, NoActionError)
from typing import (
  ClassVar,
  Type,
  Dict
)
import traceback
import logging

_log = logging.getLogger(__name__)

@registry
class GlobalErrorExtension(BaseExtension):
  LANGUAGE: ClassVar[str]
  def registry_message(self, cls: Type[Exception], key: str, /) -> None:
    self.keys[cls] = key
  async def setup(self):
    self.LANGUAGE = self.builder.PT_BR
    self.keys: Dict[Type[Exception], str] = {}
  @exception(NoActionError)
  async def on_no_action_error(self, ctx: MorkatoContext, exc: NoActionError) -> None: ...
  @exception(AppError)
  async def on_app_error(self, ctx: MorkatoContext, exc: AppError) -> None:
    reply = ctx.message if exc.reply_message else None
    kwargs = exc.parameters
    args = exc.args
    key = exc.key
    content: str
    try:
      content = (
        self.builder.get_content(self.LANGUAGE, key, *args, **kwargs)
        if not exc.is_unknown_params
        else self.builder.get_content_unknown_formatting(self.LANGUAGE, key)
      )
    except UnknownMessageContent:
      content = "Unknown message content for key: **%s.%s**" % (self.LANGUAGE, key)
    except Exception as exc:
      content = "An unexpected error occurred: %s" % type(exc).__name__
      _log.error(content + '\n%s', traceback.format_exc())
    await ctx.send(content, reference=reply)
  @exception(Exception)
  async def on_exception(self, ctx: MorkatoContext, exc: Exception) -> None:
    try:
      exc_type = type(exc)
      key = self.keys[exc_type]
      app_error = AppError(key).unkown_params()
      await self.on_app_error(ctx, app_error)
    except KeyError:
      await ctx.send("An unexpected error occurred: **%s**, notify my developer." % type(exc).__name__, reference=ctx.message)
      raise exc from None