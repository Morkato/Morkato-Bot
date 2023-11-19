from __future__ import annotations

from typing import (
  Optional,
  Generator,
  Generic,
  NoReturn,
  TypeVar,
  Union,
  
  overload,
  
  Any,
  TYPE_CHECKING
)

from itertools import chain

from ..attack import Attack
from ..art    import Art
from ..item   import Item

from ..errors import NotFoundError
from .        import etc

if TYPE_CHECKING:
  from .. import (
    ParentAttack,
    ArtAttack,
    ItemAttack,
    PlayerBreed,
    Player,
    Attack,
    Guild,
    Art,
    
    ArtType
  )

from .abc import GuildObject, Snowflake

import discord

T = TypeVar('T', bound=GuildObject)

__all__ = (
  'GuildElements',
  'Players',
  'Attacks',
  'Arts',
  'Arms'
)

class GuildElements(Generic[T]):
  def __init__(self, guild: Guild) -> None:
    self.guild = guild
    self.client = guild.client

  @property
  def id(self) -> int:
    return self.guild._id

class Arts(GuildElements[Art]):
  def __iter__(self) -> Generator[Art, Any, None]:
    for art in self.client._arts:
      if art.guild_id != self.guild.id:
        continue

      setattr(art, '_morkato_guild', self.guild)

      yield art
  
  def _raise_not_found(self) -> NoReturn:
    raise NotFoundError("Essa arte (Respiração, Kekkijutsu ou Estilo de Luta) não existe.")
    
  def _get_by_id(self, id: int) -> Art:
    result = etc.get(self, lambda art: art.id == id)

    if not result:
      self._raise_not_found()
    
    return result
  
  def _get_by_name(self, name: str) -> Art:
    fmt = lambda text: etc.strip_text(text,
      ignore_accents=True,
      ignore_empty=True,
      case_insensitive=True,
      strip_text=True
    )

    name = fmt(name)

    result = etc.get(self, lambda art: fmt(art.name) == name)

    if not result:
      self._raise_not_found()

    return result
  
  @overload
  def get(self, id: int) -> Art: ...
  @overload
  def get(self, name: str) -> Art: ...
  def get(self, obj: Optional[Union[str, int]] = None, /, *, name: Optional[str] = None, id: Optional[int] = None) -> Art:
    obj = id or name or obj

    if not isinstance(obj, (str, int)):
      raise TypeError
    
    if isinstance(obj, int):
      return self._get_by_id(obj)
    
    return self._get_by_name(obj)
  
  async def create(self, *,
    name:              str,
    type:              ArtType,
    embed_title:       Optional[str] = etc.UNDEFINED,
    embed_description: Optional[str] = etc.UNDEFINED,
    embed_url:         Optional[str] = etc.UNDEFINED
  ) -> Art:
    art = Art(
      client  = self.client,
      payload = await self.client.api.create_art(
        guild_id=self.id,
        name=name,
        type=type,
        embed_title=embed_title,
        embed_description=embed_description,
        embed_url=embed_url
      )
    )

    setattr(art, '_morkato_guild', self.guild)

    return art
  
  def drop(self, obj: Union[Snowflake, int]) -> Art:
    id = obj if isinstance(obj, int) else obj.id

    idx, art = next(((idx, art) for idx, art in enumerate(self.client._arts) if art._guild_id == self.guild._id and art._id == id), (-1, None))

    if idx == -1 or art is None:
      self._raise_not_found()

    del self.client._arts[idx]

    return art

class Items(GuildElements[Item]):
  def __iter__(self) -> Generator[Item, Any, None]:
    for item in self.client._items:
      if not item.guild_id == self.guild._id:
        continue

      setattr(item, '_morkato_guild', self.guild)

      yield item
    
  def _raise_if_not_exists(self) -> NoReturn:
    raise NotFoundError('Essa item não existe.')
  
  def _get_by_id(self, id: int) -> Item:
    result = etc.get(self, lambda item: item.id == id)

    if not result:
      self._raise_if_not_exists()
    
    return result
  
  def _get_by_name(self, name: str) -> Item:
    fmt = lambda text: etc.strip_text(text,
      ignore_accents=True,
      ignore_empty=True,
      case_insensitive=True,
      strip_text=True
    )

    name = fmt(name)

    result = etc.get(self, lambda item: fmt(item.name) == name)

    if not result:
      self._raise_if_not_exists()

    return result
  
  @overload
  def get(self, id: int, /) -> Item: ...
  @overload
  def get(self, name: str, /) -> Item: ...
  def get(self, obj: Union[str, int], /) -> Item:
    if isinstance(obj, int):
      return self._get_by_id(obj)
    
    return self._get_by_name(obj)

  async def create(self, *,
    name:              str,
    embed_title:       str          = etc.UNDEFINED,
    embed_description: str          = etc.UNDEFINED,
    embed_url:         str          = etc.UNDEFINED
  ) -> Item:
    payload = await self.client.api.create_item(
      guild_id=self.id,
      name=name,
      embed_title=embed_title,
      embed_description=embed_description,
      embed_url=embed_url
    )

    item = Item.create(self.client, payload)

    setattr(item, '_morkato_guild', self.guild)

    return item
  
  def _drop_by_id(self, id: int) -> Item:
    idx, item = next(((idx, item) for idx, item in enumerate(self.client._arms) if item.guild_id == self.guild.id and item.id == id), (-1, None))

    if idx == -1 or not item:
      self._raise_if_not_exists()
    
    del self.client._items[idx]

    return item
  
  def drop(self, obj: Union[Snowflake, int]) -> Item:
    return self._drop_by_id(obj if isinstance(obj, int) else obj.id)

class Players(GuildElements['Player']):
  @staticmethod
  def _raise_if_not_found() -> NoReturn:
    raise NotFoundError('Esse player não é registrado.')
  
  def __iter__(self) -> Generator[Player, Any, None]:
    for player in self.client._players:
      if not player._guild_id:
        continue

      setattr(player, '_morkato_guild', self.guild)

      yield player
  
  def _get_by_id(self, id: int) -> Player:
    result = etc.get(self, lambda p: p._id == id)

    if not result:
      Players._raise_if_not_found()

    return result
  
  def _get_by_member(self, member: discord.Member) -> Player:
    if member.guild.id != self.guild.id:
      Players._raise_if_not_found()
    
    result = self._get_by_id(member.id)

    setattr(result, '_morkato_member', member)

    return result
  
  def get(self, obj: Union[discord.Member, int]) -> Player:
    if isinstance(obj, int):
      return self._get_by_id(obj)
    
    return self._get_by_member(obj)
  
  async def create(self, *,
    id:          int,
    name:        str,
    breed:       PlayerBreed,
    history:     Optional[str] = etc.UNDEFINED,
    credibility: int           = etc.UNDEFINED,
    cash:        int           = etc.UNDEFINED,
    life:        int           = etc.UNDEFINED,
    breath:      int           = etc.UNDEFINED,
    blood:       int           = etc.UNDEFINED,
    resistance:  int           = etc.UNDEFINED,
    velocity:    int           = etc.UNDEFINED,
    force:       int           = etc.UNDEFINED,
    exp:         int           = etc.UNDEFINED,
    appearance:  Optional[str] = etc.UNDEFINED,
    banner:      Optional[str] = etc.UNDEFINED
  ) -> Player:
    payload = await self.client.api.create_player(
      guild_id=self.id,
      id=id,
      name=name,
      breed=breed,
      history=history,
      credibility=credibility,
      cash=cash,
      life=life,
      breath=breath,
      blood=blood,
      resistance=resistance,
      velocity=velocity,
      force=force,
      exp=exp,
      appearance=appearance,
      banner=banner
    )

    player = Player(client=self.client, payload=payload)

    setattr(player, '_morkato_guild', self.guild)

    return player
  
  def _drop_by_id(self, id: int) -> Player:
    idx, p = next(((idx, p) for idx, p in enumerate(self.client._players) if p.guild_id == self.guild.id and p.id == id), (-1, None))

    if idx == -1 or not p:
      self._raise_if_not_exists()
    
    del self.client._players[idx]

    return p
  
  def drop(self, obj: Union[Snowflake, int]) -> Player:
    return self._drop_by_id(obj if isinstance(obj, int) else obj.id)

class Attacks(GuildElements[Attack]):
  def __iter__(self) -> Generator[Attack, Any, None]:
    for attack in self.client._attacks:
      if attack.guild_id != self.guild.id:
        continue

      setattr(attack, '_morkato_guild', self.guild)

      yield attack
  
  @property
  def parent_attacks(self) -> Generator[ParentAttack, Any, Any]:
    return (atk for atk in self if atk._parent_id)
  
  @property
  def art_attacks(self) -> Generator[ArtAttack, Any, Any]:
    return (atk for atk in self if atk._art_id and not atk._parent_id)
  
  @property
  def item_attacks(self) -> Generator[ItemAttack, Any, Any]:
    return (atk for atk in self if atk._item_id)
  
  def _raise_not_found(self) -> NoReturn:
    raise NotFoundError("Esse ataque não existe.")
  
  def _get_by_id(self, id: int) -> Attack:
    result = etc.get(self, lambda attack: attack.id == id)

    if not result:
      self._raise_not_found()

    return result
  
  def _get_by_name(self, name: str) -> Union[ParentAttack, ArtAttack]:
    fmt = lambda text: etc.strip_text(text,
      ignore_accents=True,
      ignore_empty=True,
      case_insensitive=True,
      strip_text=True
    )

    name = fmt(name)

    result = etc.get(chain(self.art_attacks, self.parent_attacks), lambda attack: fmt(attack.name) == name)

    if not result:
      self._raise_not_found()

    return result
  
  def _get_by_message(self, msg: discord.Message) -> Union[ParentAttack, ArtAttack, None]:
    fmt = lambda text: etc.strip_text(text,
      ignore_accents=True,
      ignore_empty=True,
      case_insensitive=True,
      strip_text=True
    )

    content = fmt(msg.content)

    generator = (attack for attack in self.art_attacks if fmt(attack.name) in content)
    
    try:
      return max(generator, key=lambda attack: len(attack.name))
    except ValueError:
      return
    
  @overload
  def get(self, id: int) -> Attack: ...
  @overload
  def get(self, name: str) -> Union[ParentAttack, ArtAttack]: ...
  @overload
  def get(self, msg: discord.Message) -> Union[ParentAttack, ArtAttack, None]: ...
  def get(self, obj: Optional[Union[discord.Message, str, int]] = None, /, *, id: Optional[int] = None, name: Optional[str] = None, msg: Optional[discord.Message] = None) -> Union[Attack, None]:
    obj = obj or id or name or msg

    if not isinstance(obj, (discord.Message, str, int)):
      raise TypeError
    
    if isinstance(obj, int):
      return self._get_by_id(obj)
    
    if isinstance(obj, str):
      return self._get_by_name(obj)
    
    return self._get_by_message(obj)
  
  @overload
  async def create(self, *, 
    name:              str,
    art:               GuildObject,
    damage:            int           = etc.UNDEFINED,
    breath:            int           = etc.UNDEFINED,
    blood:             int           = etc.UNDEFINED,
    embed_title:       Optional[str] = etc.UNDEFINED,
    embed_description: Optional[str] = etc.UNDEFINED,
    embed_url:         Optional[str] = etc.UNDEFINED
  ) -> ArtAttack: ...
  @overload
  async def create(self, *, 
    name:              str,
    arm:               GuildObject,
    damage:            int           = etc.UNDEFINED,
    breath:            int           = etc.UNDEFINED,
    blood:             int           = etc.UNDEFINED,
    embed_title:       Optional[str] = etc.UNDEFINED,
    embed_description: Optional[str] = etc.UNDEFINED,
    embed_url:         Optional[str] = etc.UNDEFINED
  ) -> Any: ...
  @overload
  async def create(self, *, 
    name:              str,
    parent:            GuildObject,
    damage:            int           = etc.UNDEFINED,
    breath:            int           = etc.UNDEFINED,
    blood:             int           = etc.UNDEFINED,
    embed_title:       Optional[str] = etc.UNDEFINED,
    embed_description: Optional[str] = etc.UNDEFINED,
    embed_url:         Optional[str] = etc.UNDEFINED
  ) -> ParentAttack: ...
  async def create(self, *, 
    name:              str,
    parent:            GuildObject   = etc.UNDEFINED,
    art:               GuildObject   = etc.UNDEFINED,
    arm:               GuildObject   = etc.UNDEFINED,
    damage:            int           = etc.UNDEFINED,
    breath:            int           = etc.UNDEFINED,
    blood:             int           = etc.UNDEFINED,
    embed_title:       Optional[str] = etc.UNDEFINED,
    embed_description: Optional[str] = etc.UNDEFINED,
    embed_url:         Optional[str] = etc.UNDEFINED
  ) -> Attack:
    parent_id = parent if not parent else parent.id
    art_id    = art if not art else art.id
    arm_id    = arm if not arm else arm.id
    
    payload = await self.client.api.create_attack(
      guild_id=self.id,
      name=name,
      parent=parent_id,
      art_id=art_id,
      arm_id=arm_id,
      damage=damage,
      breath=breath,
      blood=blood,
      embed_title=embed_title,
      embed_description=embed_description,
      embed_url=embed_url
    )

    attack = Attack(client=self.client, payload=payload)

    setattr(attack, '_morkato_guild', self.guild)

    if art:
      setattr(attack, '_morkato_art', art)
    
    if arm:
      setattr(attack, '_morkato_arm', arm)
    
    if parent:
      setattr(attack, '_morkato_parent', parent)

    return attack
  
  @overload
  def drop(self, obj: Snowflake) -> Attack: ...
  @overload
  def drop(self, obj: int) -> Attack: ...
  def drop(self, obj: Union[Snowflake, int]) -> Attack:
    id = obj if isinstance(obj, int) else obj.id

    idx, attack = next(((idx, attack) for idx, attack in enumerate(self.client._attacks) if attack._guild_id == self.guild._id and attack._id == id), (-1, None))

    if idx == -1 or attack is None:
      self._raise_not_found()

    del self.client._attacks[idx]

    return attack
