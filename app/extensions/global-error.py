from discord.ext.commands.errors import (ConversionError, CommandInvokeError)
from morkato.ext.context import MorkatoContext
from app.errors import AppError
from morkato.ext.extension import (
  ApplicationExtension,
  extension,
  exception
)

@extension
class GlobalErrorExtension(ApplicationExtension):
  @exception(CommandInvokeError)
  async def on_command_invoke_error(self, ctx: MorkatoContext, exc: CommandInvokeError) -> None:
    original = exc.original
    if isinstance(original, AppError):
      return await self.on_app_error(ctx, original)
    elif isinstance(original, NotImplementedError):
      return await self.on_not_implemented_error(ctx, original)
    await self.on_exception(ctx, original)
  @exception(ConversionError)
  async def on_conversion_error(self, ctx: MorkatoContext, exc: ConversionError) -> None:
    original = exc.original
    if isinstance(original, AppError):
      return await self.on_app_error(ctx, original)
    elif isinstance(original, NotImplementedError):
      return await self.on_not_implemented_error(ctx, original)
    await self.on_exception(ctx, original)
  @exception(AppError)
  async def on_app_error(self, ctx: MorkatoContext, exc: AppError) -> None:
    await ctx.send(exc.message, reference=ctx.message)
  @exception(NotImplementedError)
  async def on_not_implemented_error(self, ctx: MorkatoContext, exc: NotImplementedError) -> None:
    await ctx.send("Ocorreu um erro no qual não sei lidar, perdoa-me.", reference=ctx.message)
  @exception(Exception)
  async def on_exception(self, ctx: MorkatoContext, exc: Exception) -> None:
    await ctx.send("Ocorreu um erro inesperado, favor, notifique a meu desenvolvedor (ErrorType: **`%s`**; Stack: Console)" % type(exc).__name__)
    raise exc