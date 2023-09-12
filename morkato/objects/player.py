from __future__ import annotations

from typing import (
  Optional,
  Iterator,
  Sequence,
  Union,
  
  TYPE_CHECKING,
  List
)

from .types import Player as TypePlayer, PlayerBreed

if TYPE_CHECKING:
  from ..client import MorkatoClientManager

  from .guild import Guild

from .. import (
  errors,
  utils
)

class Player:
  def __init__(
    self,
    client:  MorkatoClientManager,
    payload: TypePlayer
  ) -> None:
    self.client = client

    self._load_variables(payload)

  def _load_variables(self, payload: TypePlayer) -> None:
    self.__name        = payload['name']
    self.__credibility = payload['credibility']

    self.__guild_id = payload['guild_id']
    self.__id       = payload['id']
    self.__breed    = payload['breed']

    self.__cash = payload['cash']

    self.__life   = payload['life']
    self.__blood  = payload['blood']
    self.__breath = payload['breath']
    self.__exp    = payload['exp']

    self.__appearance = payload['appearance']
  
  def __repr__(self) -> str:
    return self.__name
  
  @property
  def name(self) -> str:
    return self.__name
  
  @property
  def credibility(self) -> int:
    return self.__credibility
  
  @property
  def guild_id(self) -> str:
    return self.__guild_id
  
  @property
  def guild(self) -> Guild:
    return self.client.database.get_guild(self.guild_id)
  
  @property
  def id(self) -> str:
    return self.__id
  
  @property
  def breed(self) -> PlayerBreed:
    return self.__breed
  
  @property
  def cash(self) -> int:
    return self.__cash
  
  @property
  def life(self) -> int:
    return self.__life
  
  @property
  def blood(self) -> int:
    return self.__blood
  
  @property
  def breath(self) -> int:
    return self.__breath
  
  @property
  def exp(self) -> int:
    return self.__exp
  
  @property
  def appearance(self) -> Union[str, None]:
    return self.__appearance
  
  async def edit(self,
    name:         Optional[str]                 = None,
    breed:        Optional[PlayerBreed]  = None,
    credibility:  Optional[int]                 = None,
    cash:         Optional[int]                 = None,
    life:         Optional[int]                 = None,
    breath:       Optional[int]                 = None,
    blood:        Optional[int]                 = None,
    exp:          Optional[int]                 = None,
    appearance:   Optional[str]                 = None
  ) -> Player:
    payload = await self.client.api.edit_player(self.guild_id, self.id,
      name=name,
      breed=breed,
      credibility=credibility,
      cash=cash,
      life=life,
      breath=breath,
      blood=blood,
      exp=exp,
      appearance=appearance
    )

    self._load_variables(payload)

    return self
  
class Players(Sequence[Player]):
  def __init__(self, *players: Player) -> None:
    self.__items = list(players)

  def __iter__(self) -> Iterator[Player]:
    return iter(self.__items)
  
  def __len__(self) -> int:
    return len(self.__items)
  
  def __getitem__(self, k: int) -> Player:
    return self.__items[k]

  def get(self, guild_id: str, id: str) -> Player:
    result = next(self.where(guild_id=guild_id, id=id), None)

    if not result:
      raise errors.NotFoundError('Você não possuí registro.')
    
    return result
  
  def add(self, *players: Player) -> None:
    if not all(isinstance(player, Player) for player in players):
      raise TypeError
    
    self.__items.extend(players)
  
  def where(
    self, *,
    guild:    Guild = utils.UNDEFINED,
    guild_id: str   = utils.UNDEFINED,
    id:       str   = utils.UNDEFINED
  ) -> utils.GenericGen[Player]:
    nis_undefined = utils.nis_undefined
    
    if nis_undefined(guild):
      guild_id = guild.id
    
    def checker(player: Player) -> bool:
      if nis_undefined(guild_id) and not player.guild_id == guild_id:
        return False
        
      if nis_undefined(id) and not player.id == id:
        return False
      
      return True
    
    
    return (player for player in self if checker(player))
    