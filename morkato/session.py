from __future__ import annotations

from typing_extensions import Self
from typing            import (
  Coroutine,
  Generator,
  Optional,  
  Generic,
  TypeVar,
  
  List,
  Any
)

from .webkit import (
  RequestContext,
  URLParameters,
  HTTPClient,
  BadRequest,
  Response,
  Request,
  URL
)

from .types import (
  PlayerBreed,
  ArtType,
  Attack,
  Player,
  Art,
  Item,
  Guild
)

from . import (
  errors,
  utils
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
        raise errors.InternalError(BadRequest(res, badRequestMessage), internalErrorMessage)
      
      elif res.status_code == 403:
        raise errors.AlreadyExistsError(alreadyExistsMessage)
      
      elif res.status_code == 404:
        raise errors.NotFoundError(notFoundMessage)
      
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

assertItemResponse = createAssert(
  notFoundMessage='Esse item não existe.',
  alreadyExistsMessage='Esse item já existe pô :V',
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
  def get_guild(self, id: int) -> CoroContext[Guild]:
    return CoroContext(self._get_guild(id))
  
  def get_arts(self, guild_id: int) -> CoroContext[List[Art]]:
    return CoroContext(self._get_arts(guild_id))
  
  def get_art(self, guild_id: int, id: int) -> CoroContext[Art]:
    return CoroContext(self._get_art(guild_id, id))

  def get_items(self, guild_id: int) -> CoroContext[List[Item]]:
    return CoroContext(self._get_items(guild_id))
  
  def get_item(self, guild_id: int, id: int) -> CoroContext[Item]:
    return CoroContext(self._get_item(guild_id, id))
  
  def get_attacks(self, guild_id: int, art_id: int = utils.UNDEFINED) -> CoroContext[List[Attack]]:
    return CoroContext(self._get_attacks(guild_id, art_id))
  
  def get_attack(self, guild_id: int, id: int) -> CoroContext[Attack]:
    return CoroContext(self._get_attack(guild_id, id))
  
  def get_player(self, guild_id: int, id: int) -> CoroContext[Player]:
    return CoroContext(self._get_player(guild_id, id))
  
  def get_players(self, guild_id: int) -> CoroContext[List[Player]]:
    return CoroContext(self._get_players(guild_id))
  
  def create_art(self, guild_id: int, *,
    name:              str,
    type:              ArtType,
    embed_title:       Optional[str] = utils.UNDEFINED,
    embed_description: Optional[str] = utils.UNDEFINED,
    embed_url:         Optional[str] = utils.UNDEFINED
  ) -> CoroContext[Art]:
    return CoroContext(self._create_art(guild_id,
      name=name,
      type=type,
      embed_title=embed_title,
      embed_description=embed_description,
      embed_url=embed_url
    ))

  def create_item(self, guild_id: int, *,
    name:              str,
    usable:            bool          = utils.UNDEFINED,
    stack:             int           = utils.UNDEFINED,
    embed_title:       Optional[str] = utils.UNDEFINED,
    embed_description: Optional[str] = utils.UNDEFINED,
    embed_url:         Optional[str] = utils.UNDEFINED
  ) -> CoroContext[Item]:
    return CoroContext(self._create_item(guild_id,
      name=name,
      usable=usable,
      stack=stack,
      embed_title=embed_title,
      embed_description=embed_description,
      embed_url=embed_url
    ))
  
  def create_attack(self, guild_id: int, *, 
    name:              str,
    parent:            str           = utils.UNDEFINED,
    damage:            int           = utils.UNDEFINED,
    breath:            int           = utils.UNDEFINED,
    blood:             int           = utils.UNDEFINED,
    art_id:            int           = utils.UNDEFINED,
    arm_id:            int           = utils.UNDEFINED,
    embed_title:       Optional[int] = utils.UNDEFINED,
    embed_description: Optional[str] = utils.UNDEFINED,
    embed_url:         Optional[str] = utils.UNDEFINED
  ) -> CoroContext[Attack]:
    return CoroContext(self._create_attack(guild_id,
      name=name,
      parent=parent,
      damage=damage,
      breath=breath,
      blood=blood,
      art_id=art_id,
      arm_id=arm_id,
      embed_title=embed_title,
      embed_description=embed_description,
      embed_url=embed_url
    ))
  
  def create_player(self, guild_id: int, *,
    id:          int,
    name:        str,
    breed:       PlayerBreed,
    history:     Optional[str] = utils.UNDEFINED,
    credibility: int           = utils.UNDEFINED,
    cash:        int           = utils.UNDEFINED,
    life:        int           = utils.UNDEFINED,
    breath:      int           = utils.UNDEFINED,
    blood:       int           = utils.UNDEFINED,
    resistance:  int           = utils.UNDEFINED,
    velocity:    int           = utils.UNDEFINED,
    exp:         int           = utils.UNDEFINED,
    force:       int           = utils.UNDEFINED,
    appearance:  Optional[str] = utils.UNDEFINED,
    banner:      Optional[str] = utils.UNDEFINED
  ) -> CoroContext[Player]:
    return CoroContext(self._create_player(guild_id,
      id=id,
      name=name,
      breath=breath,
      breed=breed,
      history=history,
      credibility=credibility,
      cash=cash,
      life=life,
      blood=blood,
      resistance=resistance,
      velocity=velocity,
      exp=exp,
      force=force,
      appearance=appearance,
      banner=banner
    ))
  
  def edit_art(self, guild_id: int, id: int, *,
    name:              str           = utils.UNDEFINED,
    type:              ArtType       = utils.UNDEFINED,
    embed_title:       Optional[str] = utils.UNDEFINED,
    embed_description: Optional[str] = utils.UNDEFINED,
    embed_url:         Optional[str] = utils.UNDEFINED
  ) -> CoroContext[Art]:
    return CoroContext(self._edit_art(guild_id, id,
      name=name,
      type=type,
      embed_title=embed_title,
      embed_description=embed_description,
      embed_url=embed_url
    ))
  
  def edit_item(self, guild_id: int, id: int, *,
    name:              str           = utils.UNDEFINED,
    usable:            bool          = utils.UNDEFINED,
    stack:             int           = utils.UNDEFINED,
    embed_title:       Optional[str] = utils.UNDEFINED,
    embed_description: Optional[str] = utils.UNDEFINED,
    embed_url:         Optional[str] = utils.UNDEFINED
  ) -> CoroContext[Item]:
    return CoroContext(self._edit_item(guild_id, id,
      name=name,
      usable=usable,
      stack=stack,
      embed_title=embed_title,
      embed_description=embed_description,
      embed_url=embed_url
    ))
  
  def edit_attack(self, guild_id: int, id: int, *, 
    name:              str           = utils.UNDEFINED,
    required_exp:      int           = utils.UNDEFINED,
    damage:            int           = utils.UNDEFINED,
    breath:            int           = utils.UNDEFINED,
    blood:             int           = utils.UNDEFINED,
    embed_title:       Optional[str] = utils.UNDEFINED,
    embed_description: Optional[str] = utils.UNDEFINED,
    embed_url:         Optional[str] = utils.UNDEFINED
  ) -> CoroContext[Attack]:
    return CoroContext(self._edit_attack(guild_id, id,
      name=name,
      damage=damage,
      breath=breath,
      blood=blood,
      embed_title=embed_title,
      required_exp=required_exp,
      embed_description=embed_description,
      embed_url=embed_url
    ))
  
  def edit_player(self, guild_id: int, id: int,
    name:         str           = utils.UNDEFINED,
    breed:        PlayerBreed   = utils.UNDEFINED,
    history:      Optional[str] = utils.UNDEFINED,
    credibility:  int           = utils.UNDEFINED,
    cash:         int           = utils.UNDEFINED,
    life:         int           = utils.UNDEFINED,
    breath:       int           = utils.UNDEFINED,
    blood:        int           = utils.UNDEFINED,
    resistance:   int           = utils.UNDEFINED,
    velocity:     int           = utils.UNDEFINED,
    exp:          int           = utils.UNDEFINED,
    force:        int           = utils.UNDEFINED,
    appearance:   Optional[str] = utils.UNDEFINED,
    banner:       Optional[str] = utils.UNDEFINED
  ) -> CoroContext[Player]:
    return CoroContext(self._edit_player(guild_id, id,
      name=name,
      breath=breath,
      breed=breed,
      history=history,
      credibility=credibility,
      cash=cash,
      life=life,
      blood=blood,
      resistance=resistance,
      velocity=velocity,
      exp=exp,
      force=force,
      appearance=appearance,
      banner=banner
    ))
  
  def del_art(self, guild_id: int, id: int) -> CoroContext[Art]:
    return CoroContext(self._del_art(guild_id=guild_id, id=id))
  
  def del_arm(self, guild_id: int, id: int) -> CoroContext[Item]:
    return CoroContext(self._del_arm(guild_id, id))

  def del_attack(self, guild_id: int, id: int) -> CoroContext[Attack]:
    return CoroContext(self._del_attack(guild_id=guild_id, id=id))
  
  def del_player(self, guild_id: int, id: int) -> CoroContext[Player]:
    return CoroContext(self._del_player(guild_id, id))
  
  async def _get_guild(self, id: int) -> Guild:
    async with self.request(Request('GET', f'/guilds/{id}')) as resp:
      await assertGuildResponse(resp)
      
      return await resp.json()
  
  async def _get_arts(self, guild_id: int) -> List[Art]:
    async with self.request(Request('GET', f'/arts/{guild_id}')) as res:
      assertArtResponse(res)

      return await res.json()
    
  async def _get_art(self, guild_id: int, id: int) -> Art:
    async with self.request(Request('GET', f'/arts/{guild_id}/{id}')) as res:
      await assertArtResponse(res)
      
      return await res.json()
  
  async def _get_items(self, guild_id: int) -> List[Item]:
    async with self.request(Request('GET', f'/items/{guild_id}')) as res:
      await assertItemResponse(res)

      return await res.json()
    
  async def _get_item(self, guild_id: int, id: int) -> Item:
    async with self.request(Request('GET', f'/items/{guild_id}/{id}')) as res:
      await assertItemResponse(res)

      return await res.json()
    
  async def _get_attacks(self, guild_id: int, art_id: int = utils.UNDEFINED) -> List[Attack]:
    params = URLParameters()

    if utils.nis_undefined(art_id):
      params.set('art_id', art_id)
    
    async with self.request(Request('GET', URL(f'/attacks/{guild_id}', parameters=params))) as res:
      await assertAttackResponse(res)
      
      return await res.json()
    
  async def _get_attack(self, guild_id: int, id: int) -> Attack:
    async with self.request(Request('GET', f'/attacks/{guild_id}/{id}')) as res:
      await assertAttackResponse(res)

      return await res.json()

  async def _get_players(self, guild_id: int) -> List[Player]:
    async with self.request(Request('GET', f'/players/{guild_id}')) as res:
      await assertPlayerResponse(res)

      return await res.json()

  async def _get_player(self, guild_id: int, id: int) -> Player:
    async with self.request(Request('GET', f'/players/{guild_id}/{id}')) as res:
      await assertPlayerResponse(res)
      
      return await res.json()

  async def _create_art(self, guild_id: int, *,
    name:              str,
    type:              ArtType,
    embed_title:       Optional[str] = utils.UNDEFINED,
    embed_description: Optional[str] = utils.UNDEFINED,
    embed_url:         Optional[str] = utils.UNDEFINED
  ) -> Art:
    nis_undefined = utils.nis_undefined

    payload = { 'name': name, 'type': type }

    if nis_undefined(embed_title):
      payload['embed_title'] = embed_title

    if nis_undefined(embed_description):
      payload['embed_description'] = embed_description

    if nis_undefined(embed_url):
      payload['embed_url'] = embed_url

    async with self.request(Request('POST', f'/arts/{guild_id}', body=payload)) as res:
      await assertArtResponse(res)
      
      return await res.json()

  async def _create_item(self, guild_id: int, *,
    name:              str,
    usable:            bool          = utils.UNDEFINED,
    stack:             int           = utils.UNDEFINED,
    embed_title:       Optional[str] = utils.UNDEFINED,
    embed_description: Optional[str] = utils.UNDEFINED,
    embed_url:         Optional[str] = utils.UNDEFINED
  ) -> Item:
    nis_undefined = utils.nis_undefined

    payload = { 'name': name }
    
    if nis_undefined(usable):
      payload['usable'] = usable

    if nis_undefined(stack):
      payload['stack'] = stack
    
    if nis_undefined(embed_title):
      payload['embed_title'] = embed_title

    if nis_undefined(embed_description):
      payload['embed_description'] = embed_description

    if nis_undefined(embed_url):
      payload['embed_url'] = embed_url

    async with self.request(Request('POST', f'/items/{guild_id}', body=payload)) as res:
      await assertItemResponse(res)

      return await res.json()

  async def _create_attack(self, guild_id: int, *, 
    name:              str,
    parent:            str = utils.UNDEFINED,
    art_id:            int = utils.UNDEFINED,
    arm_id:            int = utils.UNDEFINED,
    damage:            int = utils.UNDEFINED,
    breath:            int = utils.UNDEFINED,
    blood:             int = utils.UNDEFINED,
    embed_title:       str = utils.UNDEFINED,
    embed_description: str = utils.UNDEFINED,
    embed_url:         str = utils.UNDEFINED
  ) -> Attack:
    nis_undefined = utils.nis_undefined
    is_undefined  = utils.is_undefined
    
    payload = { 'name': name }

    if is_undefined(parent) and is_undefined(art_id) and is_undefined(arm_id):
      raise errors.ValidationError('[ValidationError] Pelo menos um parente, arte ou arma.')
    
    if nis_undefined(parent):
      payload['parent_id'] = str(parent) if not parent is None else None
    
    if nis_undefined(art_id):
      payload['art_id'] = str(art_id) if not art_id is None else None

    if nis_undefined(arm_id):
      payload['arm_id'] = str(arm_id) if not arm_id is None else None

    if nis_undefined(damage):
      payload['damage'] = damage
    
    if nis_undefined(breath):
      payload['breath'] = breath

    if nis_undefined(blood):
      payload['blood'] = blood

    if nis_undefined(embed_title):
      payload['embed_title'] = embed_title

    if nis_undefined(embed_description):
      payload['embed_description'] = embed_description

    if nis_undefined(embed_url):
      payload['embed_url'] = embed_url

    async with self.request(Request('POST', f'/attacks/{guild_id}', body=payload)) as res:
      await assertAttackResponse(res)
      
      return await res.json()
  
  async def _create_player(self, guild_id: int, *,
    id:          int,
    name:        str,
    breed:       PlayerBreed,
    history:     Optional[str] = utils.UNDEFINED,
    credibility: int           = utils.UNDEFINED,
    cash:        int           = utils.UNDEFINED,
    life:        int           = utils.UNDEFINED,
    breath:      int           = utils.UNDEFINED,
    blood:       int           = utils.UNDEFINED,
    resistance:  int           = utils.UNDEFINED,
    velocity:    int           = utils.UNDEFINED,
    exp:         int           = utils.UNDEFINED,
    force:       int           = utils.UNDEFINED,
    appearance:  Optional[str] = utils.UNDEFINED,
    banner:      Optional[str] = utils.UNDEFINED
  ) -> Player:
    nis_undefined = utils.nis_undefined
    payload = { 'id': str(id), 'name': name, 'breed': breed }

    if nis_undefined(history):
      payload['history'] = history
    
    if nis_undefined(credibility):
      payload['credibility'] = credibility
    
    if nis_undefined(cash):
      payload['cash'] = cash

    if nis_undefined(life):
      payload['life'] = life

    if nis_undefined(breath):
      payload['breath'] = breath

    if nis_undefined(blood):
      payload['blood'] = blood
    
    if nis_undefined(resistance):
      payload['resistance'] = resistance

    if nis_undefined(velocity):
      payload['velocity'] = velocity

    if nis_undefined(exp):
      payload['exp'] = exp

    if nis_undefined(force):
      payload['force'] = force
    
    if nis_undefined(appearance):
      payload['appearance'] = appearance
    
    if nis_undefined(banner):
      payload['banner'] = banner

    async with self.request(Request('POST', f'/players/{guild_id}', body=payload)) as res:
      await assertPlayerResponse(res)

      return await res.json()
    
  async def _edit_art(self, guild_id: int, id: int, *,
    name:              str           = utils.UNDEFINED,
    type:              ArtType       = utils.UNDEFINED,
    embed_title:       Optional[str] = utils.UNDEFINED,
    embed_description: Optional[str] = utils.UNDEFINED,
    embed_url:         Optional[str] = utils.UNDEFINED
  ) -> Art:
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

    async with self.request(Request('POST', f'/arts/{guild_id}/{id}', body=payload)) as res:
      await assertArtResponse(res)
      
      return await res.json()

  async def _edit_item(self, guild_id: int, id: int, *,
    name:              str           = utils.UNDEFINED,
    usable:            bool          = utils.UNDEFINED,
    stack:             int           = utils.UNDEFINED,
    embed_title:       Optional[str] = utils.UNDEFINED,
    embed_description: Optional[str] = utils.UNDEFINED,
    embed_url:         Optional[str] = utils.UNDEFINED
  ) -> Item:
    nis_undefined = utils.nis_undefined

    payload = {  }

    if nis_undefined(name):
      payload['name'] = name
    
    if nis_undefined(usable):
      payload['usable'] = usable

    if nis_undefined(stack):
      payload['stack'] = stack

    if nis_undefined(embed_title):
      payload['embed_title'] = embed_title

    if nis_undefined(embed_description):
      payload['embed_description'] = embed_description

    if nis_undefined(embed_url):
      payload['embed_url'] = embed_url

    async with self.request(Request('POST', f'/items/{guild_id}/{id}', body=payload)) as res:
      await assertItemResponse(res)

      return await res.json()
  
  async def _edit_attack(self, guild_id: int, id: int, *, 
    name:              str           = utils.UNDEFINED,
    required_exp:      int           = utils.UNDEFINED,
    damage:            int           = utils.UNDEFINED,
    breath:            int           = utils.UNDEFINED,
    blood:             int           = utils.UNDEFINED,
    embed_title:       Optional[str] = utils.UNDEFINED,
    embed_description: Optional[str] = utils.UNDEFINED,
    embed_url:         Optional[str] = utils.UNDEFINED
  ) -> Attack:
    nis_undefined = utils.nis_undefined
    payload = {  }

    if nis_undefined(name):
      payload['name'] = name

    if nis_undefined(required_exp):
      payload['required_exp'] = required_exp

    if nis_undefined(damage):
      payload['damage'] = damage
    
    if nis_undefined(breath):
      payload['breath'] = breath

    if nis_undefined(blood):
      payload['blood'] = blood

    if nis_undefined(embed_title):
      payload['embed_title'] = embed_title

    if nis_undefined(embed_description):
      payload['embed_description'] = embed_description
    
    if nis_undefined(embed_url):
      payload['embed_url'] = embed_url
    
    async with self.request(Request('POST', f'/attacks/{guild_id}/{id}', body=payload)) as res:
      await assertAttackResponse(res)

      return await res.json()
  
  async def _edit_player(self, guild_id: int, id: int,
    name:        str           = utils.UNDEFINED,
    breed:       PlayerBreed   = utils.UNDEFINED,
    history:     Optional[str] = utils.UNDEFINED,
    credibility: int           = utils.UNDEFINED,
    cash:        int           = utils.UNDEFINED,
    life:        int           = utils.UNDEFINED,
    breath:      int           = utils.UNDEFINED,
    blood:       int           = utils.UNDEFINED,
    resistance:  int           = utils.UNDEFINED,
    velocity:    int           = utils.UNDEFINED,
    exp:         int           = utils.UNDEFINED,
    force:       int           = utils.UNDEFINED,
    appearance:  Optional[str] = utils.UNDEFINED,
    banner:      Optional[str] = utils.UNDEFINED
  ) -> Player:
    nis_undefined = utils.nis_undefined
    payload = {  }

    if nis_undefined(name):
      payload['name'] = name
    
    if nis_undefined(breed):
      payload['breed'] = breed
    
    if nis_undefined(history):
      payload['history'] = history
    
    if nis_undefined(credibility):
      payload['credibility'] = credibility
    
    if nis_undefined(cash):
      payload['cash'] = cash

    if nis_undefined(life):
      payload['life'] = life

    if nis_undefined(breath):
      payload['breath'] = breath

    if nis_undefined(blood):
      payload['blood'] = blood
    
    if nis_undefined(resistance):
      payload['resistance'] = resistance

    if nis_undefined(velocity):
      payload['velocity'] = velocity

    if nis_undefined(exp):
      payload['exp'] = exp

    if nis_undefined(force):
      payload['force'] = force
    
    if nis_undefined(appearance):
      payload['appearance'] = appearance
    
    if nis_undefined(banner):
      payload['banner'] = banner

    async with self.request(Request('POST', f'/players/{guild_id}/{id}', body=payload)) as res:
      await assertPlayerResponse(res)

      return await res.json()
    
  async def _del_art(self, guild_id: int, id: int) -> Art:
    async with self.request(Request('DELETE', f'/arts/{guild_id}/{id}')) as res:
      await assertArtResponse(res)
      
      return await res.json()
    
  async def _del_item(self, guild_id: int, id: int) -> Item:
    async with self.request(Request('DELETE', f'/items/{guild_id}/{id}')) as res:
      await assertItemResponse(res)

      return await res.json()

  async def _del_attack(self, guild_id: int, id: int) -> Attack:
    async with self.request(Request('DELETE', f'/attacks/{guild_id}/{id}')) as res:
      await assertAttackResponse(res)
      
      return await res.json()
  
  async def _del_player(self, guild_id: int, id: int) -> Player:
    async with self.request(Request('DELETE', f'/players/{guild_id}/{id}')) as res:
      await assertPlayerResponse(res)

      return await res.json()