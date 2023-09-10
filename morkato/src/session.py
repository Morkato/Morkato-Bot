from __future__ import annotations

from typing_extensions import Self
from typing            import (
  Coroutine,
  Generator,
  Optional,
  Literal,
  Generic,
  TypeVar,
  
  List,
  Any
)

from webkit import (
  RequestContext,
  URLParameters,
  HTTPClient,
  BadRequest,
  Response,
  Request,
  URL
)

from objects.types import player, attack, guild, art

from errors import (
  NotFoundError,
  InternalError,
  AlreadyExistsError
)

import asyncio
import aiohttp
import logging

_log = logging.getLogger(__name__)

T = TypeVar('T')

def createAssert(*,
   notFoundMessage:      Optional[str] = None,
   alreadyExistsMessage: Optional[str] = None,
   badRequestMessage:    Optional[str] = None,
   internalErrorMessage: Optional[str] = None
):
  async def handle(res: Response) -> None:
    if not res.status_code == 200:
      if res.status_code == 400:
        raise InternalError(BadRequest(res, badRequestMessage), internalErrorMessage)
      
      elif res.status_code == 403:
        raise AlreadyExistsError(alreadyExistsMessage)
      
      elif res.status_code == 404:
        raise NotFoundError(notFoundMessage)
      
      await res.raise_for_status()
    
  return handle

assertGuildResponse = createAssert(
  notFoundMessage='Esse servidor não está configurado.',
  alreadyExistsMessage='Te passar as últimas atualizações, esse servidor já está configurado (T_T).',
  badRequestMessage='Ops, erro inesperado \'-\'.',
  internalErrorMessage='Erro interno, é complicado :/'
)

assertArtResponse = createAssert(
  notFoundMessage='Essa arte não existe.',
  alreadyExistsMessage='Essa arte já existe mano :V',
  badRequestMessage='Erro no lado do servidor.',
  internalErrorMessage='Pera, pera, mandando aqui.... E erro! Tsc, desculpe-me, erro inesperado.'
)

assertAttackResponse = createAssert(
  notFoundMessage='Esse ataque não existe.',
  alreadyExistsMessage='Esse ataque já existe.',
  badRequestMessage='Erro no lado do servidor.',
  internalErrorMessage='Aiai, vou mandar aqui.. Mandando... Mandando... E, pera, o que aconteceu? Um erro inesperado, desculpe-me.'
)

assertPlayerResponse = createAssert(
  notFoundMessage='Esse usuário não está registrado.',
  alreadyExistsMessage='Esse usuário já tem um registro.',
  badRequestMessage='Erro no lado do servidor.',
  internalErrorMessage='Bem, tentei, tentei, mas não consegui passar do erro inesperado :/ Perdoa-me.'
)

class CoroContext(Generic[T]):
  __slots__ = ('_coro', '_resp')

  def __init__(self, coro: Coroutine[Any, Any, T]) -> None:
    self._coro = coro
  
  def send(self, arg: None) -> asyncio.Future[Any]:
    return self._coro.send(arg)
  
  def throw(self, exp: Exception) -> None:
    self._coro.throw(exp)

  def close(self) -> None:
    return self._coro.close()
  
  def __await__(self) -> Generator[Any, None, T]:
    return self._coro.__await__()
  
  def __iter__(self) -> Generator[Any, None, T]:
    return self.__await__()
  
  async def __aenter__(self) -> T:
    self._resp = await self
  
    return self._resp

class BaseSessionController:
  def __init__(self, auth: str) -> None:
    self.session: HTTPClient = None # type: ignore

    self.__auth = auth
  
  async def __aenter__(self) -> Self:
    return await self.start()
  
  async def __aexit__(self, *args) -> None:
    await self.close()
  
  async def ws(self, gateway: str) -> aiohttp.ClientWebSocketResponse:
    return await self.session.ws(gateway)
  
  @property
  def base_session(self):
    return self.session._session
  
  @property
  def auth(self) -> str:
    return self.__auth

  async def start(self) -> Self:
    loop = asyncio.get_running_loop()
    
    self.session = HTTPClient(loop=loop, headers={ 'authorization': self.__auth })

    _log.info('Started Session in Morkato API')

    return self
  
  def request(self, request: Request, **kwargs) -> RequestContext:
    return self.session.request(request, **kwargs)
  
  async def close(self) -> bool:
    return await self.session.close()

class MorkatoSessionController(BaseSessionController):
  def get_guild(self, id: str) -> CoroContext[guild.Guild]:
    return CoroContext(self._get_guild(id))
  
  def get_arts(self, guild_id: str) -> CoroContext[List[art.Art]]:
    return CoroContext(self._get_arts(guild_id))
  
  def get_art(self, guild_id: str, id: str) -> CoroContext[art.Art]:
    return CoroContext(self._get_art(guild_id, id))
  
  def get_attacks(self, guild_id: str, art_id: Optional[str] = None) -> CoroContext[List[attack.Attack]]:
    return CoroContext(self._get_attacks(guild_id, art_id))
  
  def get_attack(self, guild_id: str, id: str) -> CoroContext[attack.Attack]:
    return CoroContext(self._get_attack(guild_id, id))
  
  def get_player(self, guild_id: str, id: str) -> CoroContext[player.Player]:
    return CoroContext(self._get_player(guild_id, id))
  
  def get_players(self, guild_id: str) -> CoroContext[List[player.Player]]:
    return CoroContext(self._get_players(guild_id))
  
  def create_art(self, guild_id: str, *,
    name:              str,
    type:              Literal['RESPIRATION', 'KEKKIJUTSU'],
    embed_title:       Optional[str] = None,
    embed_description: Optional[str] = None,
    embed_url:         Optional[str] = None
  ) -> CoroContext[art.Art]:
    return CoroContext(self._create_art(guild_id,
      name=name,
      type=type,
      embed_title=embed_title,
      embed_description=embed_description,
      embed_url=embed_url
    ))
  
  def create_attack(self, guild_id: str, *, 
    name:              str,
    parent:            Optional[str]       = None,
    art_id:            Optional[str]       = None,
    embed_title:       Optional[str]       = None,
    embed_description: Optional[str]       = None,
    embed_url:         Optional[str]       = None
  ) -> CoroContext[attack.Attack]:
    return CoroContext(self._create_attack(guild_id,
      name=name,
      parent=parent,
      art_id=art_id,
      embed_title=embed_title,
      embed_description=embed_description,
      embed_url=embed_url
    ))
  
  def create_player(self, guild_id: str, *,
    id:          str,
    name:        str,
    breed:       player.PlayerBreed,
    credibility: Optional[int] = None,
    cash:        Optional[int] = None,
    life:        Optional[int] = None,
    breath:      Optional[int] = None,
    blood:       Optional[int] = None,
    exp:         Optional[int] = None,
    appearance:  Optional[str] = None
  ) -> CoroContext[player.Player]:
    return CoroContext(self._create_player(guild_id,
      id=id,
      name=name,
      breath=breath,
      breed=breed,
      credibility=credibility,
      cash=cash,
      life=life,
      blood=blood,
      exp=exp,
      appearance=appearance
    ))
  
  def edit_art(self, guild_id: str, id: str, *,
    name:              Optional[str]                                  = None,
    type:              Optional[Literal['RESPIRATION', 'KEKKIJUTSU']] = None,
    embed_title:       Optional[str]                                  = None,
    embed_description: Optional[str]                                  = None,
    embed_url:         Optional[str]                                  = None
  ) -> CoroContext[art.Art]:
    return CoroContext(self._edit_art(guild_id, id,
      name=name,
      type=type,
      embed_title=embed_title,
      embed_description=embed_description,
      embed_url=embed_url
    ))
  
  def edit_attack(self, guild_id: str, id: str, *, 
    name:              Optional[str]       = None,
    required_exp:      Optional[int]       = None,
    embed_title:       Optional[str]       = None,
    embed_description: Optional[str]       = None,
    embed_url:         Optional[str]       = None
  ) -> CoroContext[attack.Attack]:
    return CoroContext(self._edit_attack(guild_id, id,
      name=name,
      embed_title=embed_title,
      required_exp=required_exp,
      embed_description=embed_description,
      embed_url=embed_url
    ))
  
  def edit_player(self, guild_id: str, id: str,
    name:         Optional[str]                = None,
    breed:        Optional[player.PlayerBreed] = None,
    credibility:  Optional[int]                = None,
    cash:         Optional[int]                = None,
    life:         Optional[int]                = None,
    breath:       Optional[int]                = None,
    blood:        Optional[int]                = None,
    exp:          Optional[int]                = None,
    appearance:   Optional[str]                = None
  ) -> CoroContext[player.Player]:
    return CoroContext(self._edit_player(guild_id, id,
      name=name,
      breath=breath,
      breed=breed,
      credibility=credibility,
      cash=cash,
      life=life,
      blood=blood,
      exp=exp,
      appearance=appearance
    ))
  
  def del_art(self, guild_id: str, id: str) -> CoroContext[art.Art]:
    return CoroContext(self._del_art(guild_id=guild_id, id=id))

  def del_attack(self, guild_id: str, id: str) -> CoroContext[attack.Attack]:
    return CoroContext(self._del_attack(guild_id=guild_id, id=id))
  
  def del_player(self, guild_id: str, id: str) -> CoroContext[player.Player]:
    return CoroContext(self._del_player(guild_id, id))
  
  async def _get_guild(self, id: str) -> guild.Guild:
    async with self.request(Request('GET', f'/guilds/{id}')) as resp:
      await assertGuildResponse(resp)
      
      return await resp.json()
  
  async def _get_arts(self, guild_id: str) -> List[art.Art]:
    async with self.request(Request('GET', f'/guilds/{guild_id}/arts')) as res:
      assertArtResponse(res)

      return await res.json()
    
  async def _get_art(self, guild_id: str, id: str) -> art.Art:
    async with self.request(Request('GET', f'/guilds/{guild_id}/arts/{id}')) as res:
      await assertArtResponse(res)
      
      return await res.json()
    
  async def _get_attacks(self, guild_id: str, art_id: Optional[str] = None) -> List[attack.Attack]:
    params = URLParameters()

    if art_id:
      params.set('art_id', art_id)
    
    async with self.request(Request('GET', URL(f'/guilds/{guild_id}/attacks', parameters=params))) as res:
      await assertAttackResponse(res)
      
      return await res.json()
    
  async def _get_attack(self, guild_id: str, id: str) -> attack.Attack:
    async with self.request(Request('GET', f'/guilds/{guild_id}/attacks/{id}')) as res:
      await assertAttackResponse(res)

      return await res.json()

  async def _get_players(self, guild_id: str) -> List[player.Player]:
    async with self.request(Request('GET', f'/guilds/{guild_id}/players')) as res:
      await assertPlayerResponse(res)

      return await res.json()

  async def _get_player(self, guild_id: str, id: str) -> player.Player:
    async with self.request(Request('GET', f'/guilds/{guild_id}/players/{id}')) as res:
      await assertPlayerResponse(res)
      
      return await res.json()

  async def _create_art(self, guild_id: str, *,
    name:              str,
    type:              Literal['RESPIRATION', 'KEKKIJUTSU'],
    embed_title:       Optional[str] = None,
    embed_description: Optional[str] = None,
    embed_url:         Optional[str] = None
  ) -> art.Art:
    payload = { 'name': name, 'type': type }

    if embed_title:
      payload['embed_title'] = embed_title

    if embed_description:
      payload['embed_description'] = embed_description

    if embed_url:
      payload['embed_url'] = embed_url

    async with self.request(Request('POST', f'/guilds/{guild_id}/arts', body=payload)) as res:
      await assertArtResponse(res)
      
      return await res.json()

  async def _create_attack(self, guild_id: str, *, 
    name:              str,
    parent:            Optional[str]       = None,
    art_id:            Optional[str]       = None,
    embed_title:       Optional[str]       = None,
    embed_description: Optional[str]       = None,
    embed_url:         Optional[str]       = None
  ) -> attack.Attack:
    payload = { 'name': name }

    if parent:
      payload['parent_id'] = parent
    
    if art_id:
      payload['art_id'] = art_id

    if embed_title:
      payload['embed_title'] = embed_title

    if embed_description:
      payload['embed_description'] = embed_description

    if embed_url:
      payload['embed_url'] = embed_url

    async with self.request(Request('POST', f'/guilds/{guild_id}/attacks', body=payload)) as res:
      await assertAttackResponse(res)
      
      return await res.json()
  
  async def _create_player(self, guild_id: str, *,
    id:          str,
    name:        str,
    breed:       player.PlayerBreed,
    credibility: Optional[int] = None,
    cash:        Optional[int] = None,
    life:        Optional[int] = None,
    breath:      Optional[int] = None,
    blood:       Optional[int] = None,
    exp:         Optional[int] = None,
    appearance:  Optional[str] = None
  ) -> player.Player:
    payload = { 'id': id, 'name': name, 'breed': breed }

    if credibility:
      payload['credibility'] = credibility
    
    if cash:
      payload['cash'] = cash

    if life:
      payload['life'] = life

    if breath:
      payload['breath'] = breath

    if blood:
      payload['blood'] = blood

    if exp:
      payload['exp'] = exp
    
    if appearance:
      payload['appearance'] = appearance

    print(payload)

    async with self.request(Request('POST', f'/guilds/{guild_id}/players', body=payload)) as res:
      await assertPlayerResponse(res)

      return await res.json()
    
  async def _edit_art(self, guild_id: str, id: str, *,
    name:              Optional[str]                                  = None,
    type:              Optional[Literal['RESPIRATION', 'KEKKIJUTSU']] = None,
    embed_title:       Optional[str]                                  = None,
    embed_description: Optional[str]                                  = None,
    embed_url:         Optional[str]                                  = None
  ) -> art.Art:
    payload = {  }
    
    if name:
      payload['name'] = name
    
    if type:
      payload['type'] = type

    if embed_title:
      payload['embed_title'] = embed_title

    if embed_description:
      payload['embed_description'] = embed_description

    if embed_url:
      payload['embed_url'] = embed_url

    async with self.request(Request('POST', f'/guilds/{guild_id}/arts/{id}', body=payload)) as res:
      await assertArtResponse(res)
      
      return await res.json()
  
  async def _edit_attack(self, guild_id: str, id: str, *, 
    name:              Optional[str]       = None,
    required_exp:      Optional[int]       = None,
    embed_title:       Optional[str]       = None,
    embed_description: Optional[str]       = None,
    embed_url:         Optional[str]       = None
  ) -> attack.Attack:
    payload = {  }

    if name:
      payload['name'] = name

    if required_exp:
      payload['required_exp'] = required_exp

    if embed_title:
      payload['embed_title'] = embed_title

    if embed_description:
      payload['embed_description'] = embed_description
    
    if embed_url:
      payload['embed_url'] = embed_url

    async with self.request(Request('POST', f'/guilds/{guild_id}/attacks/{id}', body=payload)) as res:
      await assertAttackResponse(res)

      return await res.json()
  
  async def _edit_player(self, guild_id: str, id: str,
    name:         Optional[str]                = None,
    breed:        Optional[player.PlayerBreed] = None,
    credibility:  Optional[int]                = None,
    cash:         Optional[int]                = None,
    life:         Optional[int]                = None,
    breath:       Optional[int]                = None,
    blood:        Optional[int]                = None,
    exp:          Optional[int]                = None,
    appearance:   Optional[str]                = None
  ) -> player.Player:
    payload = {  }

    if name:
      payload['name'] = name
    
    if breed:
      payload['breed'] = breed
    
    if credibility:
      payload['credibility'] = credibility
    
    if cash:
      payload['cash'] = cash

    if life:
      payload['life'] = life

    if breath:
      payload['breath'] = breath

    if blood:
      payload['blood'] = blood

    if exp:
      payload['exp'] = exp
    
    if appearance:
      payload['appearance'] = appearance

    async with self.request(Request('POST', f'/guilds/{guild_id}/players/{id}', body=payload)) as res:
      await assertPlayerResponse(res)

      return await res.json()
    
  async def _del_art(self, guild_id: str, id: str) -> art.Art:
    async with self.request(Request('DELETE', f'/guilds/{guild_id}/arts/{id}')) as res:
      await assertArtResponse(res)
      
      return await res.json()

  async def _del_attack(self, guild_id: str, id: str) -> attack.Attack:
    async with self.request(Request('DELETE', f'/guilds/{guild_id}/attacks/{id}')) as res:
      await assertAttackResponse(res)
      
      return await res.json()
  
  async def _del_player(self, guild_id: str, id: str) -> player.Player:
    async with self.request(Request('DELETE', f'/guilds/{guild_id}/players/{id}')) as res:
      await assertPlayerResponse(res)

      return await res.json()

  