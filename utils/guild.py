from typing import Callable, Literal, Optional, TypeVar, Union, overload

from errors import NotFoundError, AlrearyExistsError

from discord.guild import Guild as discordGuild, Role
from decouple import config

from .types.guild import Guild as TypedGuild
from .types.generic import Json

from .art import Attack, Art, TypedArt, toKey
from .vars import Variable

import requests

AUTH = { 'authorization': config('BOT_TOKEN') }
URL = config('URL')
T = TypeVar('T')

class GuildPayload:
  def __init__(self, discordGuild: discordGuild, payload: TypedGuild) -> None:
    self.discord = discordGuild

    self.id = payload['id']

    self.vars = [ Variable(self, data) for data in payload['vars'] ]
    
    self.created_at = payload['created_at']
    self.updated_at = payload['updated_at']

    self.cached = {}
  def __repr__(self) -> str:
    return f'Guild(id={self.id})'
  @overload
  def request_element(self, method: str, element: str, /, *, data: Optional[str] = None, json: Optional[Json] = None) -> Union[requests.Response, T]: ...
  @overload
  def request_element(self, method: str, element: str, /, *, call: Callable[[requests.Response], T], data: Optional[str] = None, json: Optional[Json] = None) -> T: ...
  def request_element(self, method: str, element: str, /, *, call: Optional[Callable[[requests.Response], T]] = None, data: Optional[str] = None, json: Optional[Json] = None) -> Union[requests.Response, T]:
    if data:
      response = requests.request(method, f'{URL}/api/bot/guilds/{self.id}/{element.strip("/")}', data=data, headers=AUTH)
    elif json:
      response = requests.request(method, f'{URL}/api/bot/guilds/{self.id}/{element.strip("/")}', json=json, headers=AUTH)
    else:
      response = requests.request(method, f'{URL}/api/bot/guilds/{self.id}/{element.strip("/")}', headers=AUTH)

    if callable(call):
      return call(response)
    return response

class Guild(GuildPayload):
  @property
  def arts(self) -> list[Art]:
    if self.cached.get('arts') is not None:
      return self.cached['arts']

    self.cached['arts'] = self.get_arts()

    return self.arts
  @property
  def attacks(self) -> list[Attack]:
    return [ attack for art in self.arts for attack in art.attacks ]

  def get_arts(self, map: Optional[Literal['RESPIRATION', 'KEKKIJUTSU']] = None) -> list[Art]:
    def check(res: requests.Response) -> list[TypedArt]:
      if not res.status_code == 200:
        res.raise_for_status()
      return res.json()
    
    if map is None:
      return [ Art(self, data) for data in self.request_element('GET', '/arts', call=check) ]
    
    return [ Art(self, data) for data in self.request_element('GET', f'/arts?map={map}', call=check) ]
  def get_art(self, art_name: str) -> Union[Art, None]:
    if self.cached.get('arts') is not None:
      return next((art for art in self.arts if toKey(art.name) == toKey(art_name)), None)
    def check(res: requests.Response) -> Union[TypedArt, None]:
      if not res.status_code == 200:
        return
      return res.json()
    
    data = self.request_element('GET', f'/arts/{art_name}', call=check)

    if data:
      return Art(self, self.request_element('GET', f'/arts/{art_name}', call=check))
  def del_art(self, name: str) -> Art:
    def check(res: requests.Response):
      if not res.status_code == 200:
        res.raise_for_status()

      return res.json()
    
    data = self.request_element('DELETE', f'/arts/{name}', call=check)

    if self.cached.get('arts') is not None:
      index, art = next(((index, art) for index, art in enumerate(self.arts) if art.name == name), (None, None))

      if art:
        del self.arts[index]

        return art

    return Art(self, data)

  def get_attack(self, attack_name: str) -> Union[Attack, None]:
    if self.cached.get('arts') is not None:
      return next((art for art in self.attacks if toKey(art.name) == toKey(attack_name)), None)
    
    def check(res: requests.Response):
      if not res.status_code == 200:
        if not res.status_code == 404:
          res.raise_for_status()
        return

      return res.json()
    
    data = self.request_element('GET', f'/attacks/{toKey(attack_name)}', call=check)

    if not data:
      return

    return Attack(self, data)
  
  def new_respiration(self, name: str) -> Art:
    def check(res: requests.Response):
      if not res.status_code == 200:
        if res.status_code == 400:
          raise AlrearyExistsError(message='Essa arte já existe.')
        res.raise_for_status()
      
      return res.json()
    art = Art(self, self.request_element('POST', '/arts', json={ "name": name, "type": 'RESPIRATION' }, call=check))

    if self.cached.get('arts') is not None:
      self.arts.append(art)

    return art
  def new_kekkijutsu(self, name: str) -> Art:
    def check(res: requests.Response):
      if not res.status_code == 200:
        if res.status_code == 400:
          raise AlrearyExistsError(message='Essa arte já existe.')
        res.raise_for_status()
      
      return res.json()
    art = Art(self, self.request_element('POST', '/arts', json={ "name": name, "type": 'KEKKIJUTSU' }, call=check))

    if self.cached.get('arts') is not None:
      self.arts.append(art)

    return art

  def new_var(self, *, name: str, text: str, roles: Optional[list[Role]] = None, required_roles: Optional[int] = None) -> Variable:
    def check(res: requests.Response):
      if not res.status_code == 200:
        if not res.status_code == 404:
          res.raise_for_status()
        res.raise_for_status()

      return res.json()
    
    payload = { 'name': name, 'text': text }

    if roles:
      payload['roles'] = [ str(role.id) for role in roles ]
    if required_roles:
      payload['required_roles'] = required_roles

    data = self.request_element('POST', '/vars', json=payload, call=check)

    var = Variable(self, data)

    self.vars.append(var)

    return var

def get(guild: discordGuild) -> Guild:
  def check(res: requests.Response) -> TypedGuild:
    if not res.status_code == 200:
      res.raise_for_status()

    return res.json()

  return Guild(guild, check(requests.get(f'{URL}/api/bot/guilds/{guild.id}', headers=AUTH)))