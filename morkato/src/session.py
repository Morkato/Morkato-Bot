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
  Request,
  URL
)

from objects.types import variable, attack, guild, art

from errors import (
  NotFoundError,
  InternalError,
  AlreadyExistsError
)

import asyncio

T = TypeVar('T')

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

  async def start(self) -> Self:
    loop = asyncio.get_running_loop()
    
    self.session = HTTPClient(loop=loop, headers={ 'authorization': self.__auth })

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
  
  def del_art(self, guild_id: str, id: str) -> CoroContext[art.Art]:
    return CoroContext(self._del_art(guild_id=guild_id, id=id))

  def del_attack(self, guild_id: str, id: str) -> CoroContext[art.Attack]:
    return CoroContext(self._del_attack(guild_id=guild_id, id=id))
  
  async def _get_guild(self, id: str) -> guild.Guild:
    async with self.request(Request('GET', f'/guilds/{id}')) as resp:
      if not resp.status_code == 200:
        if resp.status_code == 404:
          raise NotFoundError('Esse servidor não existe.')
        
        await resp.raise_for_status()
      
      return await resp.json()
  
  async def _get_arts(self, guild_id: str) -> List[art.Art]:
    async with self.request(Request('GET', f'/guilds/{guild_id}/arts')) as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Esse servidor não existe.')
        await res.raise_for_status()

      return await res.json()
    
  async def _get_art(self, guild_id: str, id: str) -> art.Art:
    async with self.request(Request('GET', f'/guilds/{guild_id}/arts/{id}')) as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Essa arte não existe.')
        
        elif res.status_code == 400:
          raise InternalError(BadRequest(res, 'Erro interno no servidor'), 'Erro interno, favor, notificar a uma desenvolvedor.')
        
        await res.raise_for_status()
      
      return await res.json()
    
  async def _get_attacks(self, guild_id: str, art_id: Optional[str] = None) -> List[attack.Attack]:
    params = URLParameters()

    if art_id:
      params.set('art_id', art_id)
    
    async with self.request(Request('GET', URL(f'/guilds/{guild_id}/attacks', parameters=params))) as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Esse ataque não existe.')
        
        elif res.status_code == 400:
          raise InternalError(BadRequest(res, 'Erro interno no servidor'), 'Erro interno, favor, notificar a uma desenvolvedor.')
        
        await res.raise_for_status()
      
      return await res.json()
    
  async def _get_attack(self, guild_id: str, id: str) -> attack.Attack:
    async with self.request(Request('GET', f'/guilds/{guild_id}/attacks/{id}')) as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Esse ataque não existe.')
        
        elif res.status_code == 400:
          raise InternalError(BadRequest(res, 'Erro interno no servidor'), 'Erro interno, favor, notificar a uma desenvolvedor.')
        
        await res.raise_for_status()

      return await res.json()

  async def create_art(self, guild_id: str, *,
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
      if not res.status_code == 200:
        if res.status_code == 409:
          raise AlreadyExistsError('Essa arte já existe.')
        
        await res.raise_for_status()
      
      return await res.json()

  async def create_variable(self, guild_id: str, *,
    name: str,
    text: str
  ) -> variable.Variable:
    payload = { 'name': name, 'text': text }

    async with self.request(Request('POST', f'/guilds/{guild_id}/vars', body=payload)) as res:
      if not res.status_code == 200:
        if res.status_code == 409:
          raise AlreadyExistsError('Essa variável já existe.')
        
        await res.raise_for_status()
      
      return await res.json()

  async def create_attack(self, guild_id: str, *, 
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
      if not res.status_code == 200:
        if res.status_code == 409:
          raise AlreadyExistsError('Esse ataque já existe.')
        
        await res.raise_for_status()
      
      return await res.json()
    
  async def edit_art(self, guild_id: str, id: str, *,
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
      if not res.status_code == 200:
        if res.status_code == 409:
          raise AlreadyExistsError('Esse ataque já existe.')
        
        await res.raise_for_status()
      
      return await res.json()
  
  async def edit_attack(self, guild_id: str, id: str, *, 
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
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Esse ataque não existe.')
        
        elif res.status_code == 400:
          raise InternalError(BadRequest(res, 'Erro interno no servidor'), 'Erro interno, favor, notificar a uma desenvolvedor.')
        
        await res.raise_for_status()

      return await res.json()
    
  async def _del_art(self, guild_id: str, id: str) -> art.Art:
    async with self.request(Request('DELETE', f'/guilds/{guild_id}/arts/{id}')) as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Essa arte não existe.')
        
        elif res.status_code == 400:
          raise InternalError(BadRequest(res, 'Erro interno no servidor'), 'Erro interno, favor, notificar a uma desenvolvedor.')
        
        await res.raise_for_status()
      
      return await res.json()

  async def _del_attack(self, guild_id: str, id: str) -> attack.Attack:
    async with self.request(Request('DELETE', f'/guilds/{guild_id}/attacks/{id}')) as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Essa arte não existe.')
        
        elif res.status_code == 400:
          raise InternalError(BadRequest(res, 'Erro interno no servidor'), 'Erro interno, favor, notificar a uma desenvolvedor.')
        
        await res.raise_for_status()
      
      return await res.json()
  