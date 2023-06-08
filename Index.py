from decouple import config

from discord import Message, Intents
from discord.ext.commands import CommandInvokeError
from discord.ext import commands
from utils import getGuild
from glob import glob

from sys import exit

from errors import InternalServerError, BaseError

class MyBot(commands.Bot):
  def __init__(self, command_prefix: str = 'man!', case_insensitive: bool = True) -> None:
    super(commands.Bot, self).__init__(
      command_prefix=command_prefix,
      intents=Intents.all(),
      case_insensitive=case_insensitive
    )
  async def on_ready(self) -> None:
    print(f'Estou conectado, como : {self.user}')
  
  async def on_command_error(self, ctx: commands.Context, err: CommandInvokeError) -> None:
    if not isinstance(err, CommandInvokeError):
      return
    error = err.original

    if isinstance(error, BaseError):
      if not isinstance(error, InternalServerError):
        await ctx.send(error.message)
    
  async def on_message(self, message: Message, /) -> None:
    if message.author.bot:
      return
    if message.content.strip().startswith('-'):
      guild = getGuild(message.guild)

      attacks = [ attack for attack in guild.attacks if attack.in_message(message.content.strip()) ]

      if attacks:
        for attack in attacks:
          await message.channel.send(embed=attack.embed_at(message.author))
    
    return await self.process_commands(message)
  async def on_edit_message(self, message: Message, /) -> None:
    return await self.on_message(message)
  
  async def setup_hook(self) -> None:
    for file in glob('Commands/*.py'):
      if file[-3:] == '.py':
        print(file[:-3].replace('/', '.'))
        await self.load_extension(file[:-3].replace('/', '.'))
  

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
