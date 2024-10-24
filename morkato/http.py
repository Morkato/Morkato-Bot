from .errors import (HTTPException, PlayerNotFoundError, NotFoundError, MorkatoServerError, MorkatoHTTPType, ModelType)
from urllib.parse import quote
from .utils import NoNullDict
from typing_extensions import Self
from typing import (
  Optional,
  ClassVar,
  SupportsInt,
  Union,
  Dict,
  List,
  Any
)
from .types import (
  Ability as AbilityPayload,
  Player as PlayerPayload,
  Family as FamilyPayload,
  Attack as AttackPayload,
  Guild as GuildPayload,
  Npc as NpcPayload,
  Art as ArtPayload,
  ArtWithAttacks,
  AbilityType,
  NpcType,
  ArtType
)

import logging
import asyncio
import aiohttp
import orjson
import sys
import os

logger = logging.getLogger(__name__)

async def json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
  text = await response.text(encoding='utf-8')
  try:
    type = response.headers['Content-Type'].split(';', 1)[0]
    if type == 'application/json':
      return orjson.loads(text)
  except KeyError:
    pass
  return text
class Route:
  BASE: ClassVar[str] = os.getenv("URL", "http://localhost:5500")
  def __init__(self, method: str, path: str, **parameters):
    self.path: str = path
    self.method: str = method
    url = self.BASE + self.path
    if parameters:
      url = url.format_map({k: quote(v) if isinstance(v, str) else v for k, v in parameters.items()})
    self.url: str = url
class HTTPClient:
  def __init__(
    self,
    loop: Optional[asyncio.AbstractEventLoop] = None,
    connector: Optional[aiohttp.BaseConnector] = None
  ) -> None:
    self.loop = loop
    self.connector = connector
    self.__session: aiohttp.ClientSession = None # type: ignore
    user_agent = 'morkato (https://github.com/morkato/morkato-Bot {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
    self.user_agent: str = user_agent.format(1.0, sys.version_info, aiohttp.__version__)
  async def __aenter__(self) -> Self:
    return self
  async def __aexit__(self, *args) -> None:
    await self.close()
  async def ws_connect(self, url: str) -> aiohttp.ClientWebSocketResponse:
    kwargs = {
      'max_msg_size': 0,
      'timeout': 30.0,
      'headers': {
          'User-Agent': self.user_agent
      },
      'autoping': False
    }
    return await self.__session.ws_connect(url, **kwargs)
  async def static_login(self) -> None:
    if self.loop is None:
      self.loop = asyncio.get_running_loop()
    if self.connector is None:
      self.connector = aiohttp.TCPConnector(limit=0)
    self.__session = aiohttp.ClientSession(
      connector=self.connector
    )
  async def close(self) -> None:
    if self.__session is not None:
      await self.__session.close()
      self.__session = None # type: ignore
  async def request(self, route: Route, **kwargs) -> Any:
    if not self.__session:
      raise NotImplementedError
    headers: Dict[str, Union[str, int]] = {
      "User-Agent": self.user_agent
    }
    if "json" in kwargs:
      headers["Content-Type"] = "application/json; charset=utf-8"
      json = kwargs.pop("json")
      kwargs["data"] = orjson.dumps(json)
    kwargs["headers"] = headers
    method = route.method
    url = route.url
    for tries in range(5):
      try:
        async with self.__session.request(method, url, **kwargs) as response:
          status = response.status
          data = await json_or_text(response)
          logger.debug("%s %s retornou: %s", method, url, status)
          if status in range(200, 300):
            return data
          extra = data.get("extra", {})
          if status == 404:
            model_name = data["model"]
            model = ModelType[model_name]
            if model == ModelType.PLAYER:
              raise PlayerNotFoundError(response, extra)
            raise NotFoundError(response, ModelType.GENERIC, extra)
          elif status >= 500:
            raise MorkatoServerError(response, extra)
          raise HTTPException(response, extra)
      except OSError as err:
        if tries < 4 and err.errno in (54, 10054):
          await asyncio.sleep(1 + tries * 2)
          continue
        raise
  async def fetch_guild(self, id: int) -> GuildPayload:
    route = Route("GET", "/guilds/{id}", id=id)
    return await self.request(route)
  async def fetch_arts(self, guild_id: int) -> List[Union[ArtWithAttacks, ArtPayload]]:
    route = Route("GET", "/arts/{gid}", gid=guild_id)
    payload = await self.request(route)
    return payload
  async def fetch_npc(self, guild_id: int, id_or_surname: Union[str, int]) -> NpcPayload:
    route = Route("GET", "/npcs/{guild_id}/{id}", guild_id=guild_id, id=id_or_surname)
    payload = await self.request(route)
    return payload
  async def fetch_player(self, guild_id: int, id: int) -> PlayerPayload:
    route = Route("GET", "/players/{guild_id}/{id}", guild_id=guild_id, id=id)
    return await self.request(route)
  async def fetch_families(self, guild_id: int) -> List[FamilyPayload]:
    route = Route("GET", "/families/{guild_id}", guild_id=guild_id)
    return await self.request(route)
  async def fetch_abilities(self, guild_id: int) -> List[AbilityPayload]:
    route = Route("GET", "/abilities/{guild_id}", guild_id=guild_id)
    return await self.request(route)
  async def create_guild(
    self, id: int, *,
    start_rpg_calendar: str,
    start_rpg_date: Optional[str] = None,
    human_initial_life: Optional[int] = None,
    oni_initial_life: Optional[int] = None,
    hybrid_initial_life: Optional[int] = None,
    breath_initial: Optional[int] = None,
    blood_initial: Optional[int] = None,
    family_roll: Optional[int] = None,
    ability_roll: Optional[int] = None,
    roll_category_id: Optional[str] = None,
    off_category_id: Optional[str] = None
  ) -> GuildPayload:
    route = Route("POST", "/guilds/{id}", id=id)
    payload = NoNullDict(
      start_rpg_calendar = start_rpg_calendar,
      start_rpg_date = start_rpg_date,
      human_initial_life = human_initial_life,
      oni_initial_life = oni_initial_life,
      hybrid_initial_life = hybrid_initial_life,
      breath_initial = breath_initial,
      blood_initial = blood_initial,
      family_roll = family_roll,
      ability_roll = ability_roll,
      roll_category_id = roll_category_id,
      off_category_id = off_category_id
    )
    return await self.request(route, json=payload)
  async def update_guild(
    self, id: int, *,
    human_initial_life: Optional[int] = None,
    oni_initial_life: Optional[int] = None,
    hybrid_initial_life: Optional[int] = None,
    breath_initial: Optional[int] = None,
    blood_initial: Optional[int] = None,
    family_roll: Optional[int] = None,
    ability_roll: Optional[int] = None,
    roll_category_id: Optional[str] = None,
    off_category_id: Optional[str] = None
  ) -> GuildPayload:
    route = Route("PUT", "/guilds/{id}", id=id)
    payload = NoNullDict(
      human_initial_life = human_initial_life,
      oni_initial_life = oni_initial_life,
      hybrid_initial_life = hybrid_initial_life,
      breath_initial = breath_initial,
      blood_initial = blood_initial,
      family_roll = family_roll,
      ability_roll = ability_roll,
      roll_category_id = roll_category_id,
      off_category_id = off_category_id
    )
    return await self.request(route, json=payload)
  async def delete_guild(self, id: int) -> GuildPayload:
    route = Route("DELETE", "/guilds/{id}", id=id)
    return await self.request(route)
  async def create_art(
    self, guild_id: int, *,
    name: str,
    type: ArtType,
    energy: Optional[int] = None,
    life: Optional[int] = None,
    breath: Optional[int] = None,
    blood: Optional[int] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> ArtPayload:
    route = Route("POST", "/arts/{gid}", gid=guild_id)
    payload = NoNullDict(
      name = name,
      type = type,
      energy = energy,
      life = life,
      breath = breath,
      blood = blood,
      description = description,
      banner = banner
    )
    return await self.request(route, json=payload)
  async def update_art(
    self, guild_id: int, id: int, *,
    name: Optional[str] = None,
    type: Optional[ArtType] = None,
    energy: Optional[int] = None,
    life: Optional[int] = None,
    breath: Optional[int] = None,
    blood: Optional[int] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> Union[ArtPayload, ArtWithAttacks]:
    route = Route("PUT", "/arts/{guild_id}/{id}", guild_id=guild_id, id=id)
    payload = NoNullDict(
      name = name,
      type = type,
      energy = energy,
      life = life,
      breath = breath,
      blood = blood,
      description = description,
      banner = banner
    )
    payload = await self.request(route, json=payload)
    return payload
  async def delete_art(self, guild_id: int, id: int) -> Union[ArtWithAttacks, ArtPayload]:
    route = Route("DELETE", "/arts/{guild_id}/{id}", guild_id=guild_id, id=id)
    return await self.request(route)
  async def create_attack(
    self, guild_id: int, art_id: int, *,
    name: str,
    name_prefix_art: Optional[str] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None,
    damage: Optional[int] = None,
    breath: Optional[int] = None,
    blood: Optional[int] = None,
    flags: Optional[SupportsInt] = None
  ) -> AttackPayload:
    route = Route("POST", "/attacks/{guild_id}/{art_id}", guild_id=guild_id, art_id=art_id)
    payload = NoNullDict(
      name = name,
      name_prefix_art = name_prefix_art,
      description = description,
      banner = banner,
      damage = damage,
      breath = breath,
      blood = blood
    )
    if flags is not None:
      payload.update(flags=int(flags))
    return await self.request(route, json=payload)
  async def update_attack(
    self, guild_id: int, id: int, *,
    name: Optional[str] = None,
    name_prefix_art: Optional[str] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None,
    damage: Optional[int] = None,
    breath: Optional[int] = None,
    blood: Optional[int] = None,
    flags: Optional[SupportsInt] = None
  ) -> AttackPayload:
    route = Route("PUT", "/attacks/{guild_id}/{id}", guild_id=guild_id, id=id)
    payload = NoNullDict(
      name = name,
      name_prefix_art = name_prefix_art,
      description = description,
      banner = banner,
      damage = damage,
      breath = breath,
      blood = blood
    )
    if flags is not None:
      payload.update(flags=int(flags))
    return await self.request(route, json=payload)
  async def delete_attack(self, guild_id: int, id: int) -> AttackPayload:
    route = Route("DELETE", "/attacks/{guild_id}/{id}", guild_id=guild_id, id=id)
    return await self.request(route)
  async def create_npc(
    self, guild_id: int, family_id: int, *,
    name: str,
    surname: str,
    type: NpcType,
    flags: Optional[SupportsInt] = None,
    icon: Optional[str] = None
  ) -> NpcPayload:
    route = Route("POST", "/npcs/{guild_id}", guild_id=guild_id)
    payload = NoNullDict(
      family_id = family_id,
      name = name,
      surname = surname,
      flags = flags,
      type = type,
      icon = icon
    )
    return await self.request(route, json=payload)
  async def update_npc(
    self, guild_id: int, id: int, *,
    name: Optional[str] = None,
    surname: Optional[str] = None,
    flags: Optional[SupportsInt] = None,
    type: Optional[NpcType] = None,
    max_life: Optional[int] = None,
    max_breath: Optional[int] = None,
    max_blood: Optional[int] = None,
    current_life: Optional[int] = None,
    current_breath: Optional[int] = None,
    current_blood: Optional[int] = None,
    last_action: Optional[int] = None,
    icon: Optional[str] = None
  ) -> NpcPayload:
    route = Route("PUT", "/npcs/{guild_id}/{id}", guild_id=guild_id, id=id)
    payload = NoNullDict(
      name = name,
      surname = surname,
      flags = flags,
      type = type,
      max_life = max_life,
      max_breath = max_breath,
      max_blood = max_blood,
      current_life = current_life,
      current_breath = current_breath,
      current_blood = current_blood,
      last_action = last_action,
      icon = icon
    )
    return await self.request(route, json=payload)
  async def create_ability(
    self, guild_id: int, *,
    name: str,
    percent: int,
    npc_kind: SupportsInt,
    energy: Optional[int] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> AbilityPayload:
    route = Route("POST", "/abilities/{guild_id}", guild_id=guild_id)
    payload = NoNullDict(
      name = name,
      energy = energy,
      percent = percent,
      npc_kind = int(npc_kind),
      description = description,
      banner = banner
    )
    return await self.request(route, json=payload)
  async def update_ability(
    self, guild_id: int, id: int, *,
    name: Optional[str] = None,
    type: Optional[AbilityType] = None,
    energy: Optional[int] = None,
    percent: Optional[int] = None,
    npc_kind: Optional[SupportsInt] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> AbilityPayload:
    route = Route("PUT", "/abilities/{guild_id}/{id}", guild_id=guild_id, id=id)
    payload = NoNullDict(
      name = name,
      type = type,
      energy = energy,
      percent = percent,
      description = description,
      banner = banner
    )
    if npc_kind is not None:
      payload.update(npc_kind=int(npc_kind))
    return await self.request(route, json=payload)
  async def delete_ability(self, guild_id: int, id: int) -> AbilityPayload:
    route = Route("DELETE", "/abilities/{guild_id}/{id}", guild_id=guild_id, id=id)
    return await self.request(route)
  async def create_family(
    self, guild_id: int, *,
    name: str,
    npc_type: int,
    percent: int,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> FamilyPayload:
    route = Route("POST", "/families/{guild_id}", guild_id=guild_id)
    payload = NoNullDict(
      name = name,
      npc_type = npc_type,
      percent = percent,
      description = description,
      banner = banner
    )
    return await self.request(route, json=payload)
  async def update_family(
    self, guild_id: int, id: int, *,
    name: Optional[str] = None,
    percent: Optional[int] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> FamilyPayload:
    route = Route("PUT", "/families/{guild_id}/{id}", guild_id=guild_id, id=id)
    payload = NoNullDict(
      name = name,
      percent = percent,
      description = description,
      banner = banner
    )
    return await self.request(route, json=payload)
  async def delete_family(self, guild_id: int, id: int) -> FamilyPayload:
    route = Route("DELETE", "/families/{guild_id}/{id}", guild_id=guild_id, id=id)
    return await self.request(route)
  async def create_player(
    self, guild_id: int, id: int, *,
    npc_kind: NpcType,
    ability_roll: Optional[int] = None,
    family_roll: Optional[int] = None,
    prodigy_roll: Optional[int] = None,
    mark_roll: Optional[int] = None,
    berserk_roll: Optional[int] = None,
    flags: Optional[SupportsInt] = None
  ) -> PlayerPayload:
    route = Route("POST", "/players/{guild_id}/{id}", guild_id=guild_id, id=id)
    payload = NoNullDict(
      expected_npc_kind = npc_kind,
      ability_roll = ability_roll,
      family_roll = family_roll,
      prodigy_roll = prodigy_roll,
      mark_roll = mark_roll,
      berserk_roll = berserk_roll
    )
    if flags is not None:
      payload["flags"] = int(flags)
    return await self.request(route, json=payload)
  async def update_player(
    self, guild_id: int, id: int, *,
    ability_roll: Optional[int] = None,
    family_roll: Optional[int] = None,
    family_id: Optional[int] = None,
    prodigy_roll: Optional[int] = None,
    mark_roll: Optional[int] = None,
    berserk_roll: Optional[int] = None,
    flags: Optional[SupportsInt] = None
  ) -> PlayerPayload:
    route = Route("PUT", "/players/{guild_id}/{id}", guild_id=guild_id, id=id)
    payload = NoNullDict(
      ability_roll = ability_roll,
      family_roll = family_roll,
      family_id = family_id,
      prodigy_roll = prodigy_roll,
      mark_roll = mark_roll,
      berserk_roll = berserk_roll
    )
    if flags is not None:
      payload["flags"] = int(flags)
    return await self.request(route, json=payload)
  async def delete_player(self, guild_id: int, id: int) -> PlayerPayload:
    route = Route("DELETE", "/players/{guild_id}/{id}", guild_id=guild_id, id=id)
    return await self.request(route)
  
  async def sync_player_family(self, guild_id: int, player_id: int, family_id: int) -> None:
    route = Route("POST", "/players/{guild_id}/{player_id}/families/{family_id}", guild_id=guild_id, player_id=player_id, family_id=family_id)
    await self.request(route)
  async def sync_player_ability(self, guild_id: int, player_id: int, ability_id: int) -> None:
    route = Route("POST", "/players/{guild_id}/{player_id}/abilities/{ability_id}", guild_id=guild_id, player_id=player_id, ability_id=ability_id)
    await self.request(route)
  async def sync_family_ability(self, guild_id: int, family_id: int, ability_id: int) -> None:
    route = Route("POST", "/families/{guild_id}/{family_id}/abilities/{ability_id}", guild_id=guild_id, family_id=family_id, ability_id=ability_id)
    await self.request(route)

  async def registry_player(self, guild_id: int, player_id: int, *, name: str, surname: str, icon: Optional[str] = None) -> PlayerPayload:
    route = Route("POST", "/players/{guild_id}/{player_id}/npc", guild_id=guild_id, player_id=player_id)
    payload = {
      "name": name,
      "surname": surname
    }
    if icon is not None:
      payload["icon"] = icon
    return await self.request(route, json=payload)