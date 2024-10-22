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
  ) -> Guild:
    payload = await self.http.create_guild(
      id = id,
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
    guild = Guild(self, id, payload)
    self._add_guild(guild)
    return guild