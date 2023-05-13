from typing import Callable, Optional, TypeVar, Union, overload

from discord.guild import Guild as discordGuild, Role

from .types.guild import Guild as TypedGuild
from .types.generic import Headers, Json

from api import Response, Route, GUILD_ID, TOKEN, session

from .respiration import Respiration, TypedRespiration

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
  
  def session(self, route: Route, headers: Optional[Headers] = None, /, **kwargs):
    return session(route.format(**kwargs, guild_id=self.id), headers or { "authorization": TOKEN })
  @overload
  def request_element(self, method: str, element: str, /, *, data: Optional[str] = None, json: Optional[Json] = None) -> Union[Response, T]: ...
  @overload
  def request_element(self, method: str, element: str, /, *, call: Callable[[Response], T], data: Optional[str] = None, json: Optional[Json] = None) -> T: ...
  def request_element(self, method: str, element: str, /, *, call: Optional[Callable[[Response], T]] = None, data: Optional[str] = None, json: Optional[Json] = None) -> Union[Response, T]:
    with self.session(GUILD_ID) as api:
      if data:
        response = api.request(method, element, data=data)
      elif json:
        response = api.request(method, element, json=json)
      else:
        response = api.request(method, element)

      if callable(call):
        return call(response)
      return response

class Guild(GuildPayload):
  @property
  def respirations(self) -> list[Respiration]:
    if self.cached.get('respiration') is not None:
      return self.cached['respiration']
    
    def check(res: Response) -> list[TypedRespiration]:
      if not res.status_code == 200:
        res.raise_for_status()
      
      return res.json()
    
    dataAllRespirations = self.request_element('GET', '/respirations', call=check)
    self.cached['respiration'] = [ Respiration(self, data) for data in dataAllRespirations ]

    return self.respirations
  
  def get_respiration(self, resp_name: str) -> Union[Respiration, None]:
    return next((respiration for respiration in self.respirations if respiration.name.lower() == resp_name.lower()), None)
  def new_respiration(
    self, name: str, *,
    role: Optional[Role] = None,
    embed_title: Optional[str] = None,
    embed_description: Optional[str] = None,
    embed_url: Optional[str] = None
  ) -> Respiration:
    payload = { "name": name, "role": role.id if role else role, "embed_title": embed_title, "embed_description": embed_description, "embed_url": embed_url }

    def check(res: Response) -> TypedRespiration:
      if not res.status_code == 200:
        res.raise_for_status()
      
      return res.json()
    
    data = self.request_element('POST', '/respirations', call=check, json=payload)

    resp = Respiration(self, data)

    if self.cached.get('respirations') is not None:
      self.respirations.append(resp)
    
    return resp

def get(guild: discordGuild) -> Guild:
  def check(res: Response) -> TypedGuild:
    if not res.status_code == 200:
      res.raise_for_status()

    return res.json()
  
  with session(GUILD_ID.format(guild_id=str(guild.id)), { "authorization": TOKEN }) as api:
    return Guild(guild, check(api.request('GET', '/')))