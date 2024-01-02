from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  ClassVar,
  Dict,
  List
)

if TYPE_CHECKING:
  from .types.player import Player as TypePlayer, PlayerBreedType
  
  from .state import MorkatoConnectionState
  from .http  import HTTPClient
  from .item  import PlayerItem
  from .guild import Guild

from datetime import datetime

class Player:
  HUMAN: ClassVar[PlayerBreedType] = 'HUMAN'
  ONI: ClassVar[PlayerBreedType] = 'ONI'
  HYBRID: ClassVar[PlayerBreedType] = 'HYBRID'

  def __init__(
    self,
    state: MorkatoConnectionState,
    guild: Guild,
    data: TypePlayer
  ) -> None:
    self.state = state
    self.guild = guild

    self._load_variables(data)
    self.clear()
  
  def __repr__(self) -> str:
    cls = self.__class__
    type = "Human" if self._breed == cls.HUMAN else "Oni" if self._breed == cls.ONI else "Hybrid"

    return f'<{cls.__name__}.{type} name={self._name!r} id={self._id}>'
  
  def _load_variables(self, data: TypePlayer) -> None:
    if int(data['guild_id']) != self.guild.id:
      raise RuntimeError
    
    self._name = data['name']
    self._id = int(data['id'])

    self._credibility = data['credibility']
    self._history = data['history']
    self._breed = data['breed']

    self._cash = data['cash']

    self._life = data['life']
    self._blood = data['blood']
    self._breath = data['breath']
    self._exp = data['exp']
    self._force = data['force']
    self._velocity = data['velocity']

    self._appearance = data['appearance']
    self._banner = data['banner']

    self._updated_at = datetime.fromtimestamp(data['updated_at'] / 1000) if data['updated_at'] is not None else None

  def clear(self) -> None:
    self._inventory: Dict[int, PlayerItem] = {  }
  
  def _get_http(self) -> HTTPClient:
    return self.state.http
  
  def _add_item(self, item: PlayerItem) -> None:
    self._inventory[item.item_id] = item
  
  @property
  def inventory(self) -> List[PlayerItem]:
    return sorted(self._inventory.values(), key=lambda item: item._created_at.timestamp())

  @property
  def name(self) -> str:
    return self._name
  
  @property
  def breed(self) -> PlayerBreedType:
    return self._breed
  
  @property
  def id(self) -> int:
    return self._id
  
  @property
  def credibility(self) -> int:
    return self._credibility
  
  @property
  def history(self) -> str:
    return self._history
  
  @property
  def cash(self) -> int:
    return self._cash
  
  @property
  def life(self) -> int:
    return self._life
  
  @property
  def breath(self) -> int:
    return self._breath
  
  @property
  def blood(self) -> int:
    return self._blood

  @property
  def exp(self) -> int:
    return self._exp
  
  @property
  def force(self) -> int:
    return self._force
  
  @property
  def velocity(self) -> int:
    return self._velocity