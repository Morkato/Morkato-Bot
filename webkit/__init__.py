from glob import glob

from discord.ext import commands
import discord

from discord.ext.commands.errors import *
from errors import *

from utils.etc import getEnv
discord.client.DiscordWebSocket
import aiohttp
import asyncio

class Bot(commands.Bot):
  LOG_CHANNEL_ID: int = int(getEnv('LOG_CHANNEL_ID', '1120029460436090901'))
  OWNER_GUILD_ID: int = int(getEnv('OWNER_GUILD_ID', '971803172056219728'))

  def __init__(self, command_prefix: str = '!', case_insensitive: bool = True) -> None:
    super(commands.Bot, self).__init__(
      command_prefix=command_prefix,
      intents=discord.Intents.all(),
      case_insensitive=case_insensitive
    )
    
  async def on_ready(self) -> None:
    await self.tree.sync()
    
    print(f'Estou conectado, como : {self.user}')
  
  async def on_command_error(self, ctx: commands.Context, err: CommandInvokeError) -> None:
    if not isinstance(err, CommandInvokeError):
      return

    error = err.original

    if isinstance(error, BaseError):
      if not isinstance(error, InternalServerError):
        await ctx.send(error.message)
    
  async def on_message(self, message: discord.Message, /) -> None:
    if message.author.bot:
      return
    
    return await self.process_commands(message)
  async def on_edit_message(self, message: discord.Message, /) -> None:
    return await self.on_message(message)
  
  async def setup_hook(self) -> None:
    for file in glob('Commands/*.py'):
      if file[-3:] == '.py':
        print(file[:-3].replace('/', '.'))
        await self.load_extension(file[:-3].replace('/', '.'))

class Client(Bot):
  WEB_SOCKET_CONNECTION: str = "ws://morkato-bot.vercel.app"

  def __init__(self, command_prefix: str = '!', case_insensitive: bool = True) -> None:
    super(Bot, self).__init__(command_prefix, case_insensitive)

    self.websocket: aiohttp.ClientWebSocketResponse = None # type: ignore
    self.db = None

  async def pollEvents(self, message: aiohttp.WSMessage) -> None:
    ...
  
  async def on_ready(self) -> None:
    loop = asyncio.get_event_loop()
    
    self.websocket.receive()

    loop.call_soon()
    
    await super().on_ready()

async def events(loop, client: Client) -> None:
  await client.pollEvents(await client.websocket.receive())

  return loop.call_later(2, events, loop, client)