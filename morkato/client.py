from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  Any,
  Set,

  Optional,
  NoReturn,
  Union,

  overload
)

if TYPE_CHECKING:
  from discord import Guild as DiscordGuild, Message
  
  from .attack import ParentAttack, ArtAttack, Attack
  from .player_item import PlayerItem
  from .player import Player
  from .guild  import Guild
  from .art    import Art
  from .item   import Item

from .session  import MorkatoSessionController
from .gateway  import MorkatoWebSocketManager
from .context  import MorkatoContext
from .tree     import Tree

from discord.ext import commands
from discord     import Intents

from glob import glob
from .    import (
  errors,
  utils
)

import asyncio
import re

import discord

class MorkatoClientManager(commands.Bot):
  def __init__(
    self,
    auth:             str,
    login:            str,
    command_prefix:   str  = utils.UNDEFINED,
    case_insensitive: bool = utils.UNDEFINED
  ) -> None:
    super(commands.Bot, self).__init__(
      command_prefix=utils.case_undefined(command_prefix, '!'),
      intents=Intents.all(),
      case_insensitive=utils.case_undefined(case_insensitive, True),
      tree_cls=Tree
    )

    self._api:      MorkatoSessionController = None # type: ignore
    self._ws_morkato:  MorkatoWebSocketManager  = None # type: ignore

    self._morkato_guilds: Set[Guild]  = set()
    self._players:        Set[Player] = set()
    self._attacks:        Set[Attack] = set()
    self._arts:           Set[Art]    = set()
    self._items:          Set[Item]   = set()
    self._player_items:   Set[PlayerItem] = set()

    self._login = login
    self.__auth = auth
  
  def _raise_if_guild_not_exists(self) -> NoReturn:
    raise errors.NotFoundError('Esse servidor requer configuração.')

  def _get_morkato_guild_by_id(self, id: int) -> Guild:
    result = utils.get(self._morkato_guilds, lambda guild: guild.id == id)

    if not result:
      self._raise_if_guild_not_exists()

    return result
    
  def _get_morkato_guild_by_guild_origin(self, guild: DiscordGuild) -> Guild:
    result = self._get_morkato_guild_by_id(guild.id)

    cache = getattr(result, '_morkato_origin', None)
    
    if not cache or cache.id != guild.id:
      setattr(result, '_morkato_origin', guild)

    return result
  
  @overload
  def get_morkato_guild(self, id: int) -> Guild: ...
  @overload
  def get_morkato_guild(self, guild: DiscordGuild) -> Guild: ...
  def get_morkato_guild(self, obj: Union[DiscordGuild, int, None] = None, *, guild: Optional[DiscordGuild] = None, id: Optional[int] = None) -> Guild:
    obj = obj or guild or id
    
    if isinstance(obj, int):
      return self._get_morkato_guild_by_id(obj)
    
    return self._get_morkato_guild_by_guild_origin(obj)
  
  async def get_context(self, origin: discord.Message) -> MorkatoContext:
    return await super().get_context(origin, cls=MorkatoContext)

  @property
  def auth(self) -> str:
    return self.__auth
  
  @property
  def api(self) -> MorkatoSessionController:
    return self._api
  
  @property
  def ws_morkato(self) -> MorkatoWebSocketManager:
    return self._ws_morkato
  
  async def __aexit__(self, *args, **kwargs) -> None:
    print('Ih, fechou')
    
    await super().__aexit__(*args, **kwargs)

    await self._ws_morkato.close()
    await self._api.close()

  async def connect_morkato(self) -> None:
    try:
      while True:
        await self._ws_morkato.poll_event()
    
    except KeyboardInterrupt: ...

  async def connect(self, *, reconnect: bool = True) -> None:
    coro_morkato = self.connect_morkato()
    coro_bot = super().connect(reconnect=reconnect)

    try:
      await asyncio.gather(coro_morkato, coro_bot)
    except Exception as err:
      coro_bot.throw(err)
      coro_morkato.throw(err)

  async def start(self, token: str, *, reconnect: bool = True) -> None:
    self._api         = await MorkatoSessionController(auth=self.__auth).start()
    self._ws_morkato  = await asyncio.wait_for(MorkatoWebSocketManager.from_client(self, login=self._login), timeout=60)

    return await super().start(token=token, reconnect=reconnect)
  
  async def on_ready(self) -> None:
    await self.tree.sync()    
    
    await self.change_presence(activity = discord.Game("Pudim. O Game (LTS)"), status = discord.Status.dnd)
    
    print(f'Estou conectado, como : {self.user}')

  async def on_message(self, message: Message) -> None:
    if message.author.bot:
      return
    
    if not message.guild and message.author.id == 510948690354110464:
      await message.author.send('Tô ligado.')
      
    if self.user.mention in message.content and message.author.id == 510948690354110464:
      await message.channel.send('Oba')
    
    return await super().on_message(message)

  async def on_command_error(self, ctx: commands.Context, err: Exception) -> None:
    if not isinstance(err, commands.errors.CommandInvokeError):
      raise err

    error = err.original

    if not isinstance(error, errors.BaseError):
      await ctx.send(f'`[{type(error).__name__}: Erro interno, desculpe-me] {error}`')

      raise err
    
    await ctx.send(error.message)

  async def setup_hook(self) -> None:
    gl = glob('extensions/*.py') + glob('extensions/**/*.py')
    
    for file in gl:
      if (
        re.match(r'extensions/app_commands/(views|ext|flags|utils|v2).*', file)
        or re.match(r'extensions/(groups|v2).*', file)
        or not file[-3:] == '.py'
      ):
        continue

      ext = file[:-3].replace('/', '.')
      print(f"[Setup] Load extension: {ext}")
      
      await self.load_extension(ext)
    
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

  @property
  def api(self):
    return self.bot.api
  
  def get_guild(self, obj: discord.Guild) -> Guild:
    return self.bot.get_morkato_guild(obj)
  
  def get_player(self, member: discord.Member) -> Player:
    return self.get_guild(member.guild).get_player(member)
  
  @overload
  def get_art(self, guild: discord.Guild, id: int) -> Art: ...
  @overload
  def get_art(self, guild: discord.Guild, name: str) -> Art: ...
  def get_art(self, guild: discord.Guild, obj: Union[str, int]) -> None:
    return self.get_guild(guild).get_art(obj)
  
  def get_attack(self, guild: discord.Guild, name: str) -> Union[ArtAttack, ParentAttack]:
    return self.get_guild(guild).get_attack(name)
