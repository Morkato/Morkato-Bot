from discord.ext import commands
from glob        import glob

from discord import Intents, Message

import discord

class Client(commands.Bot):
  def __init__(self, command_prefix: str = '!', case_insensitive: bool = True) -> None:
    super(commands.Bot, self).__init__(
      command_prefix=command_prefix,
      intents=Intents.all(),
      case_insensitive=case_insensitive
    )

    self.__controller = ()
    
  async def __aenter__(self) -> "Client":
    print('Passou por aqui')

    return await super().__aenter__()
  
  async def __aexit__(self, *args, **kwargs) -> None:
    print('Ih, fechou')

    return await super().__aexit__(*args, **kwargs)
  
  async def on_ready(self) -> None:
    await self.tree.sync()
    
    print(f'Estou conectado, como : {self.user}')
  
  async def on_command_error(self, ctx: commands.Context, err) -> None:
    raise err
    
  async def on_message(self, message: Message, /) -> None:
    if message.author.bot:
      return
    
    return await self.process_commands(message)
  
  async def setup_hook(self) -> None:
    for file in glob('Commands/*.py'):
      if file[-3:] == '.py' and not '_utils.' in file:
        await self.load_extension(file[:-3].replace('/', '.'))