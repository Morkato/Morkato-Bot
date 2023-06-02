from typing import Callable, Optional, TypeVar, Union, overload

from discord.guild import Guild as discordGuild
from decouple import config
from unidecode import unidecode

from .types.guild import Guild as TypedGuild
from .types.generic import Headers, Json

import requests

AUTH = { 'authorization': config('BOT_TOKEN') }
URL = config('URL')
T = TypeVar('T')

class GuildPayload:
  def __init__(self, discordGuild: discordGuild, payload: TypedGuild) -> None:
    self.discord = discordGuild

    self.id = payload['id']
    
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

class Guild(GuildPayload): ...

def get(guild: discordGuild) -> Guild:
  def check(res: Response) -> TypedGuild:
    if not res.status_code == 200:
      res.raise_for_status()

    return res.json()
  
  with session(GUILD_ID.format(guild_id=str(guild.id)), { "authorization": TOKEN }) as api:
    return Guild(guild, check(api.request('GET', '/')))