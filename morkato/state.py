from __future__ import annotations
from .utils import CircularDict
from .http import HTTPClient
from .guild import Guild
from typing import (
  Callable,
  Optional
)

class MorkatoConnectionState:
  def __init__(self, dispatch: Callable[..., None], *, http: HTTPClient) -> None:
    self.dispatch = dispatch
    self.http = http
    self.clear()
  def clear(self) -> None:
    self._guilds: CircularDict[int, Guild] = CircularDict(32)
  def get_cached_guild(self, id: int) -> Optional[Guild]:
    return self._guilds.get(id)
  def _add_guild(self, guild: Guild) -> None:
    self._guilds[guild.id] = guild
  async def fetch_guild(self, id: int) -> Guild:
    payload = await self.http.fetch_guild(id)
    guild = Guild(self, id, payload)
    self._add_guild(guild)
    return guild