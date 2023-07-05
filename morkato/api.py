from __future__ import annotations

from typing import Optional, Literal, List, TYPE_CHECKING

from webkit.http    import HTTPClient
from webkit.errors  import BadRequest
from webkit.request import Request

from utils.string import toKey

from errors import NotFoundError, InternalError, AlreadyExistsError

import asyncio

if TYPE_CHECKING:
  from utils.art   import TypedArt, TypedAttack
  from utils.vars  import typedVariable
  from utils.guild import TypedGuild

class MorkatoAPIController:
  def __init__(self, loop: asyncio.AbstractEventLoop, auth: str) -> None:
    self.http: HTTPClient = None # type: ignore

    self.loop = loop
    self.__auth = auth

  async def __aenter__(self) -> MorkatoAPIController:
    self.http = HTTPClient(loop=self.loop, headers={ 'authorization': self.__auth })

    return self
  
  async def __aexit__(self, *args, **kwargs) -> None:
    await self.http.close()

  async def get_guild(self, id: str) -> TypedGuild:
    request = await self.http.request(Request('GET', f'/api/bot/guilds/{id}'))
    
    async with request as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Esse servidor não existe.')
        await res.raise_for_status()
      
      return await res.json()

  async def get_arts(self, guild_id: str) -> List[TypedArt]:
    request = await self.http.request(Request('GET', f'/api/bot/guilds/{guild_id}/arts'))

    async with request as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Esse servidor não existe.')
        await res.raise_for_status()

      return await res.json()
    
  async def get_art(self, guild_id: str, name: str) -> TypedArt:
    request = await self.http.request(Request('GET', f'/api/bot/guilds/{guild_id}/arts/{toKey(name)}'))

    async with request as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Essa arte não existe.')
        
        elif res.status_code == 400:
          raise InternalError(BadRequest(res, 'Erro interno no servidor'), 'Erro interno, favor, notificar a uma desenvolvedor.')
        
        await res.raise_for_status()
      
      return await res.json()
  
  async def get_attacks(self, guild_id: str, art_name: str) -> List[TypedAttack]:
    request = await self.http.request(Request('GET', f'/api/bot/guilds/{guild_id}/arts/{toKey(art_name)}/attacks'))

    async with request as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Essa arte não existe.')
        
        elif res.status_code == 400:
          raise InternalError(BadRequest(res, 'Erro interno no servidor'), 'Erro interno, favor, notificar a uma desenvolvedor.')
        
        await res.raise_for_status()
      
      return await res.json()
    
  async def get_attack(self, guild_id: str, name: str) -> TypedAttack:
    request = await self.http.request(Request('GET', f'/api/bot/guilds/{guild_id}/attacks/{toKey(name)}'))

    async with request as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Esse ataque não existe.')
        
        elif res.status_code == 400:
          raise InternalError(BadRequest(res, 'Erro interno no servidor'), 'Erro interno, favor, notificar a uma desenvolvedor.')
        
        await res.raise_for_status()

      return await res.json()
    
  async def create_art(self, guild_id: str, *,
    name: str,                               type: Literal['RESPIRATION', 'KEKKIJUTSU'],
    role: Optional[str] = None,              embed_title: Optional[str] = None,
    embed_description: Optional[str] = None, embed_url: Optional[str] = None
  ) -> TypedArt:
    payload = { 'name': name, 'type': type }

    if role:
      payload['role'] = role

    if embed_title:
      payload['embed_title'] = embed_title

    if embed_description:
      payload['embed_description'] = embed_description

    if embed_url:
      payload['embed_url'] = embed_url
    
    request = await self.http.request(Request('POST', f'/api/bot/guilds/{guild_id}/arts'), json=payload)

    async with request as res:
      if not res.status_code == 200:
        if res.status_code == 409:
          raise AlreadyExistsError('Essa arte já existe.')
        
        await res.raise_for_status()
      
      return await res.json()


  async def create_variable(self, guild_id: str, *, name: str, text: str) -> typedVariable:
    payload = { 'name': name, 'text': text }

    request = await self.http.request(Request('POST', f'/api/bot/guilds/{guild_id}/vars', body=payload))

    async with request as res:
      if not res.status_code == 200:
        if res.status_code == 409:
          raise AlreadyExistsError('Essa variável já existe.')
        
        await res.raise_for_status()
      
      return await res.json()

  async def create_attack(self, guild_id: str, art_name: str, *, 
    name:  str,
    roles: Optional[str] = None,
    embed_title: Optional[str] = None,
    embed_description: Optional[str] = None,
    embed_url: Optional[str] = None,
    damage: Optional[int] = None,
    stamina: Optional[int] = None
  ) -> TypedAttack:
    payload = { 'name': name }

    if roles:
      payload['roles'] = roles

    if embed_title:
      payload['embed_title'] = embed_title

    if embed_description:
      payload['embed_description'] = embed_description

    if embed_url:
      payload['embed_url'] = embed_url

    if damage is not None:
      payload['damage'] = damage

    if stamina is not None:
      payload['stamina'] = stamina

    request = await self.http.request(Request('POST', f'/api/bot/guilds/{guild_id}/arts/{toKey(art_name)}/attacks'))

    async with request as res:
      if not res.status_code == 200:
        if res.status_code == 409:
          raise AlreadyExistsError('Esse ataque já existe.')
        
        await res.raise_for_status()
      
      return await res.json()