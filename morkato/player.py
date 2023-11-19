from __future__ import annotations

from typing_extensions import Self
from typing            import (
  Optional,
  NoReturn,
  Generator,
  Union,
  
  TYPE_CHECKING,

  List,
  Set,
  Any
)

from numerize.numerize import numerize as num_fmt
from .errors           import NotFoundError
from .                 import utils

if TYPE_CHECKING:
  from .types  import PlayerBreed, Player as TypePlayer
  from .client import MorkatoClientManager

  from .utils.abc import Snowflake

  from .player_item import PlayerItem
  from .guild import Guild

import discord  

HUMAN_FORMAT_TEXT = """# ─ ﹒ `👦 ꒰ {name}` ! 
> **:books::  __`História`__ ~ {history}⸝⸝**
**
煤 ㅡ `❤￤Vida`  ~ __`{life}`__
煤 ㅡ `💨￤Fôlego`  ~ __`{breath}`__
煤 ㅡ `🛡️￤Resistência`  ~ __`{resistance}`__
煤 ㅡ `💪￤Força`  ~ __`{force}kg`__
煤 ㅡ `⚡￤Velocidade`  ~ __`{velocity}km/h`__

煤 ㅡ `💸￤Dinheiro`  ~ __`{cash}rm`__
煤 ㅡ `🍃￤Experiência`  ~ __`{exp}exp`__
煤 ㅡ `💍￤Credibilidade`  ~ __`{credibility}`__

煤 ㅡ `🌟￤Missão`  ~ __`Em desenvolvimento`__
煤 ㅡ `🌻￤Organização`  ~ __`Em desenvolvimento`__
煤 ㅡ `💧￤Físico`  ~ __`Em desenvolvimento`__
煤 ㅡ `⛩️￤Carreira`  ~ __`Em desenvolvimento`__
**"""

ONI_FORMAT_TEXT = """# ─ ﹒ `👹 ꒰ {name}` ! 
> **:books::  __`História`__ ~ {history}⸝⸝**
**
煤 ㅡ `❤￤Vida`  ~ __`{life}`__
煤 ㅡ `🩸￤Sangue`  ~ __`{blood}`__
煤 ㅡ `🛡️￤Resistência`  ~ __`{resistance}`__
煤 ㅡ `💪￤Força`  ~ __`{force}kg`__
煤 ㅡ `⚡￤Velocidade`  ~ __`{velocity}km/h`__

煤 ㅡ `💸￤Dinheiro`  ~ __`{cash}rm`__
煤 ㅡ `🍃￤Experiência`  ~ __`{exp}exp`__
煤 ㅡ `💍￤Credibilidade`  ~ __`{credibility}`__

煤 ㅡ `🌟￤Missão`  ~ __`Em desenvolvimento`__
煤 ㅡ `🌻￤Organização`  ~ __`Em desenvolvimento`__
煤 ㅡ `💧￤Físico`  ~ __`Em desenvolvimento`__
煤 ㅡ `⛩️￤Carreira`  ~ __`Em desenvolvimento`__
**"""

HYBRID_FORMAT_TEXT = """# ─ ﹒ `🌓 ꒰ {name}` ! 
> **:books::  __`História`__ ~ {history}⸝⸝**
**
煤 ㅡ `❤￤Vida`  ~ __`{life}`__
煤 ㅡ `💨￤Fôlego`  ~ __`{breath}`__
煤 ㅡ `🩸￤Sangue`  ~ __`{blood}`__
煤 ㅡ `🛡️￤Resistência`  ~ __`{resistance}`__
煤 ㅡ `💪￤Força`  ~ __`{force}kg`__
煤 ㅡ `⚡￤Velocidade`  ~ __`{velocity}km/h`__

煤 ㅡ `💸￤Dinheiro`  ~ __`{cash}rm`__
煤 ㅡ `🍃￤Experiência`  ~ __`{exp}exp`__
煤 ㅡ `💍￤Credibilidade`  ~ __`{credibility}`__

煤 ㅡ `🌟￤Missão`  ~ __`Em desenvolvimento`__
煤 ㅡ `🌻￤Organização`  ~ __`Em desenvolvimento`__
煤 ㅡ `💧￤Físico`  ~ __`Em desenvolvimento`__
煤 ㅡ `⛩️￤Carreira`  ~ __`Em desenvolvimento`__
**"""

class Player:
  ITEMS: Set[Player] = set()

  @staticmethod
  def get(guild: Union[Snowflake, int], usr: Union[Snowflake, int]) -> Union[Player, None]:
    guild_id = guild if isinstance(guild, int) else guild.id
    id = usr if isinstance(usr, int) else usr.id

    unique = hash((guild_id, id))

    return utils.get(Player.ITEMS, lambda p: hash(p) == unique)
  
  @staticmethod
  def create(client:  MorkatoClientManager, payload: TypePlayer) -> Player:
    player = Player.get(int(payload['guild_id']), int(payload['id']))

    if not player:
      player = Player(client, payload)

      Player.ITEMS.add(player)

    return player

  @staticmethod
  def _raise_if_not_found(p: Snowflake) -> NoReturn:
    raise NotFoundError(f'Não foi possível localizar o membro com o ID: **`{p.id}`**')

  def __init__(
    self,
    client:  MorkatoClientManager,
    payload: TypePlayer
  ) -> None:
    self._client = client

    self._morkato_guild: Union[Guild, None] = None
    self._morkato_member: Union[discord.Member, None] = None
    
    self._load_variables(payload)

    self._inv = PlayerInventory(self)
  
  def __hash__(self) -> int:
    return hash((self._guild_id, self._id))

  def _load_variables(self, payload: TypePlayer) -> None:
    self._name        = payload['name']
    self._credibility = payload['credibility']
    self._history     = payload['history']

    self._guild_id = int(payload['guild_id'])
    self._id       = int(payload['id'])
    self._breed    = payload['breed']

    self._cash = payload['cash']

    self._life       = payload['life']
    self._blood      = payload['blood']
    self._breath     = payload['breath']
    self._exp        = payload['exp']
    self._force      = payload['force']
    self._resistance = payload['resistance']
    self._velocity   = payload['velocity']

    self._appearance = payload['appearance']
    self._banner     = payload['banner']
  
  def __repr__(self) -> str:
    return f"<Player name={self._name!r} life={self._life} breath={self._breath} blood={self._blood}>"
  
  @property
  def guild(self) -> Guild:
    if not self._morkato_guild:
      self._morkato_guild = self._client.get_morkato_guild(self._guild_id)
    
    if self._morkato_guild.id != self._guild_id:
      self._morkato_guild = None

      return self.guild
    
    return self._morkato_guild
  
  @property
  def origin(self) -> discord.Member:
    if not self._morkato_member:
      self._morkato_member = self.guild.origin.get_member(self._id)

      if not self._morkato_member:
        Player._raise_if_not_found(self)

    if self._morkato_member.id != self._id:
      self._morkato_member = None

      return self.origin
    
    return self._morkato_member
  
  @property
  def inventory(self) -> PlayerInventory:
    return self._inv
  
  @property
  def guild_id(self) -> int:
    return self._guild_id

  @property
  def name(self) -> str:
    return self._name
  
  @property
  def id(self) -> int:
    return self._id
  
  @property
  def breed(self) -> PlayerBreed:
    return self._breed
  
  @property
  def cash(self) -> int:
    return self._cash
  
  @property
  def life(self) -> int:
    return self._life
  
  @property
  def blood(self) -> int:
    return self._blood
  
  @property
  def breath(self) -> int:
    return self._breath
  
  @property
  def exp(self) -> int:
    return self._exp
  
  @property
  def force(self) -> int:
    return self._force
  
  @property
  def resistance(self) -> int:
    return self._resistance
  
  @property
  def velocity(self) -> int:
    return self._velocity
  
  @property
  def appearance(self) -> Union[str, None]:
    return self._appearance
  
  @property
  def banner(self) -> Union[str, None]:
    return self._banner
  
  @property
  def embed(self) -> discord.Embed:
    formatter, color = (
      (HUMAN_FORMAT_TEXT, 3066993)
      if self.breed == 'HUMAN'
      else (
        (ONI_FORMAT_TEXT, 10038562)
        if self.breed == 'ONI'
        else (HYBRID_FORMAT_TEXT, 3447003)
      )
    )
    
    embed = discord.Embed(
      description=formatter.format(
        name=self._name,
        history=self._history or "Ele(a) nasceu, fim.",
        life=num_fmt(self._life),
        breath=num_fmt(self._breath),
        blood=num_fmt(self._blood),
        resistance=num_fmt(self._resistance),
        force=self._force,
        velocity=self._velocity,
        cash=self._cash,
        exp=self._exp,
        credibility=self._credibility
      ),
      color=color
    )

    embed.set_thumbnail(url = self.appearance or self.member.display_avatar.url)

    embed.set_footer(text = f'ID: {self.id}', icon_url = self.origin.display_avatar.url)

    if self.banner:
      embed.set_image(url=self.banner)

    return embed
  
  async def edit(self,
    name:         str           = utils.UNDEFINED,
    breed:        PlayerBreed   = utils.UNDEFINED,
    history:      Optional[str] = utils.UNDEFINED,
    credibility:  int           = utils.UNDEFINED,
    cash:         int           = utils.UNDEFINED,
    life:         int           = utils.UNDEFINED,
    breath:       int           = utils.UNDEFINED,
    blood:        int           = utils.UNDEFINED,
    resistance:   int           = utils.UNDEFINED,
    velocity:     int           = utils.UNDEFINED,
    exp:          int           = utils.UNDEFINED,
    force:        int           = utils.UNDEFINED,
    appearance:   Optional[str] = utils.UNDEFINED,
    banner:       Optional[str] = utils.UNDEFINED
  ) -> Self:
    payload = await self._client.api.edit_player(self.guild_id, self.id,
      name=name,
      breed=breed,
      credibility=credibility,
      history=history,
      cash=cash,
      life=life,
      breath=breath,
      blood=blood,
      resistance=resistance,
      velocity=velocity,
      exp=exp,
      force=force,
      appearance=appearance,
      banner=banner
    )

    self._load_variables(payload)

    return self

  async def delete(self) -> Self:
    payload = await self._client.api.del_player(self._guild_id, self._id)

    self._load_variables(payload)

    return self

class PlayerInventory:
  def __init__(self, player: Player) -> None:
    self._client = player._client
    
    self._player_id = player._id
    self._player = player

    self._guild_id = player._guild_id
  
  def __iter__(self) -> Generator[PlayerItem, Any, None]:
    for item in self._client._player_items:
      if item._guild_id != self._guild_id and item._player_id != self._player_id:
        continue

      setattr(item, '_morkato_player', self._player)
      
      yield item
  
  def __repr__(self) -> str:
    headers = f'<PlayerInventory player={self._player.name!r}\n  '
    items = '\n  '.join(map(str, self))

    if items:
      return headers + items + '\n>'
    
    return headers.strip('\n  ') + '>'
  
  @property
  def embeds(self) -> List[discord.Embed]:
    embed = discord.Embed(
      description="Para usar um item, basta dar o comando: **`!item -u <name>`**\nPara equipar um item, basta dar o comando: **`!item -e <name>`**"
    )

    for item in self:
      embed.add_field(name=f'{item.item.name}: {item._stack}', value=item.item.description or 'No description')

    embed.set_author(name = self._player.name, icon_url=self._player._appearance or self._player.origin.display_avatar.url)
    
    return [embed,]
