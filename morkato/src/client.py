from __future__ import annotations

from typing import (
  NoReturn,
  
  Any
)

from .session  import MorkatoSessionController
from .database import MorkatoDatabaseManager
from .gateway  import MorkatoWebSocketManager, WebSocketClosure

from discord.ext import commands
from discord     import Intents

from errors    import BaseError
from glob      import glob

import asyncio
import aiohttp
import re

import discord

class MorkatoClientManager(commands.Bot):
  def __init__(self, auth: str, command_prefix: str = '!', case_insensitive: bool = True) -> None:
    super(commands.Bot, self).__init__(
      command_prefix=command_prefix,
      intents=Intents.all(),
      case_insensitive=case_insensitive
    )

    self.__api:      MorkatoSessionController = None # type: ignore
    self.__database: MorkatoDatabaseManager   = None # type: ignore
    self.__gateway:  MorkatoWebSocketManager  = None # type: ignore

    self.logs_channel: discord.TextChannel  = None # type: ignore

    self.__auth = auth

  @property
  def auth(self) -> str:
    return self.__auth
  
  async def __aexit__(self, *args, **kwargs) -> None:
    print('Ih, fechou')
    
    await self.close_morkato()
    
    await super().__aexit__(*args, **kwargs)

  async def handle_event(self, e: str, d: Any) -> None:
    event = self.__gateway.get_event(e)
    
    if not event:
      return
    
    return await event(self, d)

  async def start_morkato(self) -> MorkatoWebSocketManager:
    api      = await MorkatoSessionController(auth=self.__auth).start()
    gateway  = await MorkatoWebSocketManager.from_session(api)
    database = await MorkatoDatabaseManager.from_gateway(self, gateway)

    self.__api      = api
    self.__gateway  = gateway
    self.__database = database

    return gateway

  async def close_morkato(self) -> bool:
    res_gateway = await self.__gateway.close()
    res_api = await self.__api.close()

    return res_gateway and res_api

  async def start(self, token: str, *, reconnect: bool = True) -> None:
    task_discord = asyncio.create_task(super().start(token, reconnect=reconnect))
    task_morkato = asyncio.create_task(self.pool_events(await self.start_morkato()))

    return await asyncio.gather(task_discord, task_morkato)
  
  
  @property
  def api(self) -> MorkatoSessionController:
    return self.__api
  
  @property
  def gateway(self) -> MorkatoWebSocketManager:
    return self.__gateway

  @property
  def database(self) -> MorkatoDatabaseManager:
    return self.__database
  
  async def on_ready(self) -> None:
    await self.tree.sync()

    guild = self.get_guild(971803172056219728)
    
    self.logs_channel = guild.get_channel(1147560459298410526)
    
    print(f'Estou conectado, como : {self.user}')

  async def pool_event(self, gateway: MorkatoWebSocketManager) -> None:
    (event, data) = await gateway.pool_event()

    await self.handle_event(event, data)
  
  async def pool_events(self, gateway: MorkatoWebSocketManager) -> None:
    try:
      while not gateway.closed:
        
        await self.pool_event(gateway)
    except WebSocketClosure:
      await self.close_morkato()

      for tries in range(1, 6):
        wait = 1.4 * tries * 5

        print(F"Websocket foi desconectado! Tentando uma nova conexão em {wait}s")

        await asyncio.sleep(wait)

        try:
          gateway = await self.start_morkato()

          print("Uma nova conexão foi criada!")

          await self.pool_events(gateway)
        except: ...
    print("Websocket foi desconectado, tente estabelecer uma nova conexão manualmente.")

  async def on_command_error(self, ctx: commands.Context, err: Exception) -> None:
    if not isinstance(err, commands.errors.CommandInvokeError):
      raise err

    error = err.original

    if not isinstance(error, BaseError):
      await ctx.send(f'Desculpe-me um erro insperado. Comunique a um desenvolvedor, tipo `{type(error).__name__}`, novamente, desculpe-me.')

      raise error
    
    await ctx.send(error.message)
  
  async def setup_hook(self) -> None:
    for file in glob('commands/*.py'):
      if re.match(r'commands/(ext|flags|utils)/.*', file):
        continue

      if file[-3:] == '.py':
        await self.load_extension(file[:-3].replace('/', '.'))

class MorkatoBot(MorkatoClientManager):
  """
    Uma simples classe em que controla a API do MorkatoBOT e sincroniza com o banco de dados de forma assíncrona.

    Parâmetros:
      auth (str): Código de autorização para acessar a API Morkato Bot (Requerido)

      command_prefix (str): Prefixo dos comandos (Default: "!")
      case_insensitive (bool): Para o bot ignorar letras em minusculas ou maiúsculas em comandos (Default: True)

    Propriedades:

      api      (MorkatoSessionController): Gerenciador da API Morkato Bot.
      gateway  (MorkatoWebSocketManager) : Web socket que sincroniza dados (Artes, Ataques, Servidores e Players) com o banco de dados.
      database (MorkatoDatabaseManager)  : Gerenciador do banco de dados (Artes, Ataques, Servidores e Players).

    Funcionalidades Extras:
      
      - O bot irá pegar todos os comandos via Cog de uma pasta chamada "commands" ele irá ignorar totalmente pastas chamadas: "ext", "utils" e "flags"
    
    Exemplos de Uso:

    >>> bot = MorkatoBot(auth=...)

    >>> bot.run(TOKEN)
  """

  pass

class Cog(commands.Cog):
  def __init__(self, bot: MorkatoBot) -> None:
    self.bot = bot

    self.database = bot.database
    self.gateway  = bot.gateway
    self.api      = bot.api
