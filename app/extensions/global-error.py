from aiohttp.client_exceptions import ClientConnectorError
from morkato.work.builder import UnknownMessageContent
from morkato.work.context import MorkatoContext
from morkato.work.extension import exception
from morkato.work.project import registry
from app.extension import BaseExtension
from app.errors import AppError
from typing import (
  ClassVar
)

@registry
class GlobalErrorExtension(BaseExtension):
  LANGUAGE: ClassVar[str]
  async def setup(self):
    self.LANGUAGE = self.builder.PT_BR
  @exception(AppError)
  async def on_app_error(self, ctx: MorkatoContext, exc: AppError) -> None:
    content = exc.build(self.builder, self.LANGUAGE)
    await ctx.send(content, reference=ctx.message)
  @exception(UnknownMessageContent)
  async def on_unknown_message_content(self, ctx: MorkatoContext, exc: UnknownMessageContent) -> None:
    await ctx.send("Unknown message content for key: **`%s.%s`**" % (exc.language, exc.key))
  @exception(ClientConnectorError)
  async def on_client_connector_error(self, ctx: MorkatoContext, exc: ClientConnectorError) -> None:
    exception = AppError("errorMorkatoAPIRatedServiceDoNotListening")
    await self.on_app_error(ctx, exception)
  @exception(Exception)
  async def on_exception(self, ctx: MorkatoContext, exc: Exception) -> None:
    exc_type = type(exc)
    await ctx.send("**`[%s repr(exc): %s] Ocorreu um erro inesperado. Favor, notificar ao meu desenvolvedor.`**" % (f"{exc_type.__module__}.{exc_type.__name__}", getattr(exc, "message", None)), reference=ctx.message)
    raise exc