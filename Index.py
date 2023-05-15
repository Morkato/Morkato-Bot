from decouple import config

from discord import Message, Intents
from discord.ext import commands
from glob import glob

from sys import exit

from errors import InternalServerError, BaseError

class MyBot(commands.Bot):
  def __init__(self, command_prefix: str = '!', case_insensitive: bool = True) -> None:
    super(commands.Bot, self).__init__(
      command_prefix=command_prefix,
      intents=Intents.all(),
      case_insensitive=case_insensitive
    )
  async def on_ready(self) -> None:
    print(f'Estou conectado, como : {self.user}')
    
  async def on_message(self, message: Message, /) -> None:
    return await self.process_commands(message)
  async def on_edit_message(self, message: Message, /) -> None:
    return await self.on_message(message)
  
  async def setup_hook(self) -> None:
    for file in glob('Commands/*.py'):
      if file[-3:] == '.py':
        print(file[:-3].replace('/', '.'))
        await self.load_extension(file[:-3].replace('/', '.'))
  async def on_command_error(self, ctx: commands.Context, exception: commands.CommandInvokeError) -> None:
    if isinstance(exception, commands.CommandInvokeError):
      exception = exception.original
    if isinstance(exception, BaseError):
      message = exception.message
      action = exception.action
      embeds = exception.embeds

      if isinstance(exception, InternalServerError):
        error = exception.error

        await ctx.reply(f'**Opps! Rolou um erro inesperado: `{type(error).__name__}`. Olhe a mensagem: `{message}` Tente: `{action}` Perdoa-me pelo mail entendido .-. Aceite um :custard: pelo mal entendido.**', embeds=embeds)

        return
      
      await ctx.reply(message, embeds=embeds)

      return
    
    return await self.on_command_error(ctx, InternalServerError(exception, "Um erro desconhecido.", "Relatar ao meu desenvolvedor."))

def main() -> int:
  bot = MyBot()

  try:
    TOKEN: str = config('BOT_TOKEN')
  except:
    print('Insira no ".env" uma chave chamada: BOT_TOKEN com seu token do discord.')

    return -1

  bot.run(TOKEN)
  
  return 0

if __name__ == '__main__':
  exit(main())
