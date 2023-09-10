from __future__ import annotations

from typing import (
  Optional,
  Generator,
  Literal,
  Iterator,
  Sequence,
  Union,
  
  TYPE_CHECKING,
  List,
  Any
)

from ..types import player

PlayerBreed = player.PlayerBreed

if TYPE_CHECKING:
  from morkato.client import MorkatoClientManager

  from .guild import Guild

from easy_pil   import load_image_async
from io         import BytesIO
from utils.card import card

from errors import NotFoundError

import discord

class Player:
  def __init__(
    self,
    client:  MorkatoClientManager,
    payload: player.Player
  ) -> None:
    self.client = client

    self._load_variables(payload)

  def _load_variables(self, payload: player.Player) -> None:
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
  def user(self) -> Union[discord.User, None]:
    return self.client.get_user(self.__id)
  
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
  def breed(self) -> player.PlayerBreed:
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
    breed:        Optional[player.PlayerBreed]  = None,
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

  async def card(self, member: discord.Member) -> BytesIO:
    user = member or self.user
    
    display_card = card(
      avatar_image=await load_image_async(self.appearance or user.display_avatar.url),
      breed=self.breed,
      username=member.name,
      name=self.name,
      life=self.life,
      breath=self.breath,
      blood=self.blood,
      credibility=self.credibility,
      exp=self.exp
    )

    return display_card.image_bytes
  
class Players(Sequence[Player]):
  def __init__(self, *players: List[Player]) -> None:
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
      raise NotFoundError('Você não possuí registro.')
    
    return result
  
  def add(self, player: Player) -> None:
    if not isinstance(player, Player):
      raise TypeError
    
    self.__items.append(player)
  
  def where(
    self, *,
    guild:    Optional[Guild] = None,
    guild_id: Optional[str]   = None,
    id:       Optional[str]   = None
  ) -> Generator[Player]:
    if guild:
      guild_id = guild.id
    
    def checker(player: Player) -> bool:
      if guild_id and not player.guild_id == guild_id:
        return False
        
      if id and not player.id == id:
        return False
      
      return True
    
    
    return (player for player in self if checker(player))
    