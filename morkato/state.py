from __future__ import annotations
from .http import HTTPClient, Route
from .utils import CircularDict
from .ability import Ability
from .family import Family
from .attack import Attack
from .guild import Guild
from .art import Art
from .types import (
  Ability as AbilityPayload,
  Family as FamilyPayload,
  Attack as AttackPayload,
  Npc as NpcPayload,
  Art as ArtPayload,
  ArtWithAttacks,
  AbilityType,
  NpcType,
  ArtType
)
from typing import (
  SupportsInt,
  Callable,
  Optional,
  Union,
  Dict,
  List,
  Any
)

class MorkatoConnectionState:
  def __init__(self, dispatch: Callable[..., None], *, http: HTTPClient) -> None:
    self.dispatch = dispatch
    self.http = http
    self.clear()
  def clear(self) -> None:
    self._guilds: CircularDict[int, Guild] = CircularDict(8)
  def get_cached_guild(self, id: int) -> Optional[Guild]:
    return self._guilds.get(id)
  def create_guild(self, id: int) -> Guild:
    guild = Guild(self, id)
    self._guilds[guild.id] = guild
    return guild
  async def request(self, route: Route, **kwargs) -> Any:
    return await self.http.request(route, **kwargs)
  async def fetch_arts(self, guild_id: int) -> List[Union[ArtWithAttacks, ArtPayload]]:
    route = Route("GET", "/arts/{gid}", gid=guild_id)
    payload = await self.request(route)
    return payload
  async def fetch_npc(self, guild_id: int, id_or_surname: Union[str, int]) -> NpcPayload:
    route = Route("GET", "/npcs/{guild_id}/{id}", guild_id=guild_id, id=id_or_surname)
    payload = await self.request(route)
    return payload
  async def fetch_families(self, guild_id: int) -> List[FamilyPayload]:
    route = Route("GET", "/families/{guild_id}", guild_id=guild_id)
    payload = await self.request(route)
    return payload
  async def fetch_abilities(self, guild_id: int) -> List[AbilityPayload]:
    route = Route("GET", "/abilities/{guild_id}", guild_id=guild_id)
    payload = await self.request(route)
    return payload
  async def create_art(self, guild_id: int, *, name: str, type: ArtType, description: Optional[str] = None, banner: Optional[str] = None) -> ArtPayload:
    route = Route("POST", "/arts/{gid}", gid=guild_id)
    payload = {
      "name": name,
      "type": type
    }
    if description is not None:
      payload.update(description=description)
    if banner is not None:
      payload.update(banner=banner)
    payload = await self.request(route, json=payload)
    return payload
  async def update_art(self, guild_id: int, id: int, *, name: Optional[str] = None, type: Optional[ArtType] = None, description: Optional[str] = None, banner: Optional[str] = None) -> Union[ArtPayload, ArtWithAttacks]:
    route = Route("PUT", "/arts/{guild_id}/{id}", guild_id=guild_id, id=id)
    payload = {}
    if name is not None:
      payload.update(name=name)
    if type is not None:
      payload.update(type=type)
    if description is not None:
      payload.update(description=description)
    if banner is not None:
      payload.update(banner=banner)
    payload = await self.request(route, json=payload)
    return payload
  async def delete_art(self, guild_id: int, id: int) -> Union[ArtWithAttacks, ArtPayload]:
    route = Route("DELETE", "/arts/{guild_id}/{id}", guild_id=guild_id, id=id)
    payload = await self.request(route)
    return payload
  async def create_attack(self,
    guild_id: int,
    art_id: int, *,
    name: str,
    name_prefix_art: Optional[str] = None,
    description: Optional[str] = None,
    resume_description: Optional[str] = None,
    banner: Optional[str] = None,
    damage: Optional[int] = None,
    breath: Optional[int] = None,
    blood: Optional[int] = None,
    intents: Optional[SupportsInt] = None
  ) -> AttackPayload:
    route = Route("POST", "/attacks/{guild_id}/{art_id}", guild_id=guild_id, art_id=art_id)
    payload = {
      "name": name
    }
    if name_prefix_art is not None:
      payload.update(name_prefix_art=name_prefix_art)
    if description is not None:
      payload.update(description=description)
    if resume_description is not None:
      payload.update(resume_description=resume_description)
    if banner is not None:
      payload.update(banner=banner)
    if damage is not None:
      payload.update(damage=damage)
    if breath is not None:
      payload.update(breath=breath)
    if blood is not None:
      payload.update(blood=blood)
    if intents is not None:
      payload.update(intents=int(intents))
    payload = await self.request(route, json=payload)
    return payload
  async def update_attack(self,
    guild_id: int,
    id: int, *,
    name: Optional[str] = None,
    name_prefix_art: Optional[str] = None,
    description: Optional[str] = None,
    resume_description: Optional[str] = None,
    banner: Optional[str] = None,
    damage: Optional[int] = None,
    breath: Optional[int] = None,
    blood: Optional[int] = None,
    intents: Optional[SupportsInt] = None
  ) -> AttackPayload:
    route = Route("PUT", "/attacks/{guild_id}/{id}", guild_id=guild_id, id=id)
    payload = {}
    if name is not None:
      payload.update(name=name)
    if name_prefix_art is not None:
      payload.update(name_prefix_art=name_prefix_art)
    if description is not None:
      payload.update(description=description)
    if resume_description is not None:
      payload.update(resume_description=resume_description)
    if banner is not None:
      payload.update(banner=banner)
    if damage is not None:
      payload.update(damage=damage)
    if breath is not None:
      payload.update(breath=breath)
    if blood is not None:
      payload.update(blood=blood)
    if intents is not None:
      payload.update(intents=int(intents))
    payload = await self.request(route, json=payload)
    return payload
  async def delete_attack(self, guild_id: int, id: int) -> AttackPayload:
    route = Route("DELETE", "/attacks/{guild_id}/{id}", guild_id=guild_id, id=id)
    payload = await self.request(route)
    return payload
  async def create_npc(self,
    guild_id: int, *,
    name: str,
    surname: str,
    type: NpcType,
    family_id: Optional[int] = None,
    icon: Optional[str] = None
  ) -> NpcPayload:
    route = Route("POST", "/npcs/{guild_id}", guild_id=guild_id)
    payload = {
      "name": name,
      "surname": surname,
      "type": type
    }
    if family_id is not None:
      payload.update(family_id=family_id)
    if icon is not None:
      payload.update(icon=icon)
    payload = await self.request(route, json=payload)
    return payload
  async def create_ability(
    self, guild_id: int, *,
    name: str,
    type: AbilityType,
    percent: int,
    npc_kind: SupportsInt,
    immutable: Optional[bool] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> AbilityPayload:
    payload = {
      "name": name,
      "type": type,
      "percent": percent,
      "npc_kind": int(npc_kind)
    }
    if immutable is not None:
      payload.update(immutable=immutable)
    if description is not None:
      payload.update(description=description)
    if banner is not None:
      payload.update(banner=banner)
    route = Route("POST", "/abilities/{guild_id}", guild_id=guild_id)
    payload = await self.request(route, json=payload)
    return payload
  async def update_ability(
    self, guild_id: int, id: int, *,
    name: Optional[str] = None,
    type: Optional[AbilityType],
    npc_kind: Optional[SupportsInt] = None,
    description: Optional[str] = None,
    banner: Optional[str] = None
  ) -> AbilityPayload:
    payload: Dict[str, Any] = {}
    if name is not None:
      payload.update(name=name)
    if type is not None:
      payload.update(type=type)
    if npc_kind is not None:
      payload.update(npc_kind=int(npc_kind))
    if description is not None:
      payload.update(description=description)
    if banner is not None:
      payload.update(banner=banner)
    route = Route("PUT", "/abilities/{guild_id}/{id}", guild_id=guild_id, id=id)
    payload = await self.request(route, json=payload)
    return payload
  async def delete_ability(self, guild_id: int, id: int) -> AbilityPayload:
    route = Route("DELETE", "/abilities/{guild_id}/{id}", guild_id=guild_id, id=id)
    payload = await self.request(route)
    return payload
  async def create_family(self, guild_id: int, *, name: str, description: Optional[str] = None, banner: Optional[str] = None) -> FamilyPayload:
    payload: Dict[str, Any] = {
      "name": name
    }
    if description is not None:
      payload.update(description=description)
    if banner is not None:
      payload.update(banner=banner)
    route = Route("POST", "/families/{guild_id}", guild_id=guild_id)
    payload = await self.request(route, json=payload)
    return payload
  async def update_family(self, guild_id: int, id: int, *, name: Optional[str] = None, description: Optional[str] = None, banner: Optional[str] = None) -> FamilyPayload:
    payload: Dict[str, Any] = {}
    if name is not None:
      payload.update(name=name)
    if description is not None:
      payload.update(description=description)
    if banner is not None:
      payload.update(banner=banner)
    route = Route("PUT", "/families/{guild_id}/{id}", guild_id=guild_id, id=id)
    payload = await self.request(route, json=payload)
    return payload
  async def delete_family(self, guild_id: int, id: int) -> FamilyPayload:
    route = Route("DELETE", "/families/{guild_id}/{id}", guild_id=guild_id, id=id)
    payload = await self.request(route)
    return payload
