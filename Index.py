from decouple import config

from discord.ext.commands import CommandInvokeError
from discord import Message, Intents
from discord.ext import commands
from utils import getGuild
from glob import glob

from sys import exit

from errors import InternalServerError, BaseError

import discord

class MyBot(commands.Bot):
  def __init__(self, command_prefix: str = '!', case_insensitive: bool = True) -> None:
    super(commands.Bot, self).__init__(
      command_prefix=command_prefix,
      intents=Intents.all(),
      case_insensitive=case_insensitive
    )

    self.channel: discord.TextChannel | None = None
    
  async def on_ready(self) -> None:
    await self.tree.sync()

    guild = self.get_guild(971803172056219728)

    if guild:
      self.channel = guild.get_channel(1120029460436090901)

      if self.channel:
        await self.channel.send('**`Starting websocket...`**')
        await self.channel.send('**Starting from `ws://morkato-bot.vercel.app` with authorization `admin`**')
        await self.channel.send('**Push context guild data**')

        await self.channel.send(f'**Successfully getting all guilds `{[getGuild(guild)]}`**')
        await self.channel.send('Websocket will be closed when shutting down the bot')
    
    print(f'Estou conectado, como : {self.user}')
  
  async def on_command_error(self, ctx: commands.Context, err: CommandInvokeError) -> None:
    if not isinstance(err, CommandInvokeError):
      raise err
    error = err.original

    if isinstance(error, BaseError):
      await ctx.send(error.message)

      return
    
    await ctx.send(f'**`{error}`: {getattr(error, "message", "No message")}**')
    
  async def on_message(self, message: Message, /) -> None:
    if message.author.bot:
      return
    
    return await self.process_commands(message)
  async def on_edit_message(self, message: Message, /) -> None:
    return await self.on_message(message)
  
  async def setup_hook(self) -> None:
    for file in glob('Commands/*.py'):
      if file[-3:] == '.py':
        print(file[:-3].replace('/', '.'))
        await self.load_extension(file[:-3].replace('/', '.'))

  async def close(self) -> None:
    if not self.is_closed():
      
      return super(commands.Bot, self).close()
  

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
