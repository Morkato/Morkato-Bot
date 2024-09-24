from __future__ import annotations
from typing_extensions import Self
from .utils import NoNullDict
from typing import (
  TYPE_CHECKING,
  Optional,
  Dict
)
if TYPE_CHECKING:
  from .types import (
    Family as FamilyPayload
  )
  from .state import MorkatoConnectionState
  from .ability import Ability
  from .abc import Snowflake
  from .guild import Guild

class Family:
  def __init__(self, state: MorkatoConnectionState, guild: Guild, payload: FamilyPayload) -> None:
    self.state = state
    self.guild = guild
    self.id = int(payload["id"])
    self.from_payload(payload)
    self.clear()
  def _add_ability(self, ability: Ability) -> None:
    self._abilities[ability.id] = ability
  def _del_ability(self, ability: Snowflake) -> None:
    self._abilities.pop(ability.id, None)
  def from_payload(self, payload: FamilyPayload) -> None:
    self.name = payload["name"]
    self.description = payload["description"]
    self.banner = payload["banner"]
  def clear(self) -> None:
    self._abilities: Dict[int, Ability] = {}
  def get_ability(self, id: int, /) -> Optional[Ability]:
    return self._abilities.get(id)
  async def update(self, *, name: Optional[str] = None, description: Optional[str] = None, banner: Optional[str] = None) -> Self:
    payload = NoNullDict(
      name=name,
      description=description,
      banner=banner
    )
    if payload:
      payload = await self.state.update_family(self.guild.id, self.id, **payload)
      self.from_payload(payload)
    return self
  async def delete(self) -> Self:
    payload = await self.state.delete_family(self.guild.id, self.id)
    self.from_payload(payload)
    self.guild._del_family(self)
    return self