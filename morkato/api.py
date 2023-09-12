"""
@deprecated
"""

from __future__ import annotations

from typing import Optional, Literal, List, TYPE_CHECKING

from webkit.http    import HTTPClient
from webkit.errors  import BadRequest
from webkit.request import Request, URL, URLParameters

from utils.string import toKey

from errors import NotFoundError, InternalError, AlreadyExistsError

from utils.coro import CoroContext

import asyncio

if TYPE_CHECKING:
  from objects.types import (
    art,
    guild,
    attack,
    variable
  )

class MorkatoAPIController:
  def __init__(self, loop: asyncio.AbstractEventLoop, auth: str) -> None:
    self.http: HTTPClient = None # type: ignore

    self.loop = loop
    self.__auth = auth

  async def __aenter__(self) -> MorkatoAPIController:
    return await self.start()
  
  async def __aexit__(self, *args, **kwargs) -> None:
    return await self.close()
  
  async def start(self) -> MorkatoAPIController:
    self.http = HTTPClient(loop=self.loop, headers={ 'authorization': self.__auth })

    return self
  
  async def close(self) -> None:
    return await self.http.close()
  
  def get_guild(self, id: str) -> CoroContext[guild.Guild]:
    return CoroContext(self._get_guild(id=id))
  
  def get_arts(self, guild_id: str) -> CoroContext[List[art.Art]]:
    return CoroContext(self._get_arts(guild_id=guild_id))
  
  def get_art(self, guild_id: str, name: str) -> CoroContext[art.Art]:
    return CoroContext(self._get_art(guild_id=guild_id, name=name))
  
  def get_attacks(self, guild_id: str, art_name: Optional[str] = None) -> CoroContext[List[attack.Attack]]:
    return CoroContext(self._get_attacks(guild_id=guild_id, art_name=art_name))
  
  def get_attacks_by_parents(self, guild_id: str, name: str) -> CoroContext[List[attack.Attack]]:
    return CoroContext(self._get_attacks_by_parents(guild_id=guild_id, name=name))
  
  def get_attack(self, guild_id: str, name: str) -> CoroContext[attack.Attack]:
    return CoroContext(self._get_attack(guild_id=guild_id, name=name))
  
  def del_art(self, guild_id: str, name: str) -> CoroContext[art.Art]:
    return CoroContext(self._del_art(guild_id=guild_id, name=name))

  async def _get_guild(self, id: str) -> guild.Guild:
    async with self.http.request(Request('GET', f'/guilds/{id}')) as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Esse servidor não existe.')
        await res.raise_for_status()
      
      return await res.json()

  async def _get_arts(self, guild_id: str) -> List[art.Art]:
    async with self.http.request(Request('GET', f'/guilds/{guild_id}/arts')) as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Esse servidor não existe.')
        await res.raise_for_status()

      return await res.json()
    
  async def _get_art(self, guild_id: str, name: str) -> art.Art:
    async with self.http.request(Request('GET', f'/guilds/{guild_id}/arts/{toKey(name)}')) as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Essa arte não existe.')
        
        elif res.status_code == 400:
          raise InternalError(BadRequest(res, 'Erro interno no servidor'), 'Erro interno, favor, notificar a uma desenvolvedor.')
        
        await res.raise_for_status()
      
      return await res.json()
  
  async def _get_attacks_by_parents(self, guild_id: str, name: str) -> List[attack.Attack]:
    async with self.http.request(Request('GET', f'/guilds/{guild_id}/attacks/{toKey(name)}/parents')) as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Esse ataque não existe.')
        
        elif res.status_code == 400:
          raise InternalError(BadRequest(res, 'Erro interno no servidor'), 'Erro interno, favor, notificar a uma desenvolvedor.')
        
        await res.raise_for_status()

      return await res.json()

  async def _get_attacks(self, guild_id: str, art_name: Optional[str] = None) -> List[attack.Attack]:
    params = URLParameters()

    if art_name:
      params.set('art_name', art_name)
    
    async with self.http.request(Request('GET', URL(f'/guilds/{guild_id}/attacks', parameters=params))) as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Esse ataque não existe.')
        
        elif res.status_code == 400:
          raise InternalError(BadRequest(res, 'Erro interno no servidor'), 'Erro interno, favor, notificar a uma desenvolvedor.')
        
        await res.raise_for_status()
      
      return await res.json()
    
  async def _get_attack(self, guild_id: str, name: str) -> attack.Attack:
    async with self.http.request(Request('GET', f'/guilds/{guild_id}/attacks/{toKey(name)}')) as res:
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
    role:              Optional[str] = None,
    embed_title:       Optional[str] = None,
    embed_description: Optional[str] = None,
    embed_url:         Optional[str] = None
  ) -> art.dArt:
    payload = { 'name': name, 'type': type }

    if role:
      payload['role'] = role

    if embed_title:
      payload['embed_title'] = embed_title

    if embed_description:
      payload['embed_description'] = embed_description

    if embed_url:
      payload['embed_url'] = embed_url

    async with self.http.request(Request('POST', f'/guilds/{guild_id}/arts', body=payload)) as res:
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

    async with self.http.request(Request('POST', f'/guilds/{guild_id}/vars', body=payload)) as res:
      if not res.status_code == 200:
        if res.status_code == 409:
          raise AlreadyExistsError('Essa variável já existe.')
        
        await res.raise_for_status()
      
      return await res.json()

  async def create_attack(self, guild_id: str, *, 
    name:              str,
    parent:            Optional[str]       = None,
    art_name:          Optional[str]       = None,
    roles:             Optional[List[str]] = None,
    embed_title:       Optional[str]       = None,
    embed_description: Optional[str]       = None,
    embed_url:         Optional[str]       = None,
    damage:            Optional[int]       = None,
    stamina:           Optional[int]       = None
  ) -> attack.Attack:
    payload = { 'name': name }

    if parent:
      payload['parent_key'] = parent
    
    if art_name:
      payload['art_key'] = art_name

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

    async with self.http.request(Request('POST', f'/guilds/{guild_id}/attacks', body=payload)) as res:
      if not res.status_code == 200:
        if res.status_code == 409:
          raise AlreadyExistsError('Esse ataque já existe.')
        
        await res.raise_for_status()
      
      return await res.json()
    
  async def edit_art(self, guild_id: str, art_name: str, *,
    name:              Optional[str]                                  = None,
    type:              Optional[Literal['RESPIRATION', 'KEKKIJUTSU']] = None,
    role:              Optional[str]                                  = None,
    embed_title:       Optional[str]                                  = None,
    embed_description: Optional[str]                                  = None,
    embed_url:         Optional[str]                                  = None
  ) -> art.Art:
    payload = {  }
    
    if name:
      payload['name'] = name
    
    if type:
      payload['type'] = type

    if role:
      payload['role'] = role

    if embed_title:
      payload['embed_title'] = embed_title

    if embed_description:
      payload['embed_description'] = embed_description

    if embed_url:
      payload['embed_url'] = embed_url

    async with self.http.request(Request('POST', f'/guilds/{guild_id}/arts/{toKey(art_name)}', body=payload)) as res:
      if not res.status_code == 200:
        if res.status_code == 409:
          raise AlreadyExistsError('Esse ataque já existe.')
        
        await res.raise_for_status()
      
      return await res.json()
  
  async def edit_attack(self, guild_id: str, attack_name: str, *, 
    name:              Optional[str]       = None,
    roles:             Optional[List[str]] = None,
    required_roles:    Optional[int]       = None,
    required_exp:      Optional[int]       = None,
    damage:            Optional[int]       = None,
    stamina:           Optional[int]       = None,
    embed_title:       Optional[str]       = None,
    embed_description: Optional[str]       = None,
    embed_url:         Optional[str]       = None
  ) -> attack.Attack:
    payload = {  }

    if name:
      payload['name'] = name

    if roles:
      payload['roles'] = roles

    if required_roles:
      payload['required_roles'] = required_roles

    if required_exp:
      payload['required_exp'] = required_exp

    if damage:
      payload['damage'] = damage

    if stamina:
      payload['stamina'] = stamina

    if embed_title:
      payload['embed_title'] = embed_title

    if embed_description:
      payload['embed_description'] = embed_description
    
    if embed_url:
      payload['embed_url'] = embed_url

    async with self.http.request(Request('POST', f'/guilds/{guild_id}/attacks/{toKey(attack_name)}', body=payload)) as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Esse ataque não existe.')
        
        elif res.status_code == 400:
          raise InternalError(BadRequest(res, 'Erro interno no servidor'), 'Erro interno, favor, notificar a uma desenvolvedor.')
        
        await res.raise_for_status()

      return await res.json()
  
  async def _del_art(self, guild_id: str, name: str) -> art.Art:
    async with self.http.request(Request('DELETE', f'/guilds/{guild_id}/arts/{toKey(name)}')) as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Essa arte não existe.')
        
        elif res.status_code == 400:
          raise InternalError(BadRequest(res, 'Erro interno no servidor'), 'Erro interno, favor, notificar a uma desenvolvedor.')
        
        await res.raise_for_status()
      
      return await res.json()
    
  def del_attack(self, guild_id: str, name: str) -> CoroContext[art.Attack]:
    return CoroContext(self._del_attack(guild_id=guild_id, name=name))

  async def _del_attack(self, guild_id: str, name: str) -> attack.Attack:
    async with self.http.request(Request('DELETE', f'/guilds/{guild_id}/attacks/{toKey(name)}')) as res:
      if not res.status_code == 200:
        if res.status_code == 404:
          raise NotFoundError('Essa arte não existe.')
        
        elif res.status_code == 400:
          raise InternalError(BadRequest(res, 'Erro interno no servidor'), 'Erro interno, favor, notificar a uma desenvolvedor.')
        
        await res.raise_for_status()
      
      return await res.json()