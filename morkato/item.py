from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  ClassVar,
  Optional,
  Union,
  Dict,
  List
)

if TYPE_CHECKING:
  from typing_extensions import Self

  from .types.item import Item as TypeItem, PlayerItem as TypePlayerItem
  
  from .state import MorkatoConnectionState
  from .player import Player
  from .http  import HTTPClient
  from .guild import Guild

from discord.embeds import Embed

from .errors import ErrorType, geterr
from .attack import ItemAttack
from .http   import Route
from .utils.etc import (
  attack_format_discord,
  format_text,
  get,
  fmt
)

from datetime import datetime

class Item:
  LIMIT_PAGE: ClassVar[int] = 10

  FOOTER_STYLE: ClassVar[str] = "ID: {self.id}"
  ATTACK_FORMATTER_STYLE: ClassVar[str] = "{index}° - !a `{item.name}: {attack.name}`"
  DEFAULT_DESCRIPTION: ClassVar[str] = "No description"

  def __init__(
    self,
    state: MorkatoConnectionState,
    guild: Guild,
    data: TypeItem
  ) -> None:
    self.state = state
    self.guild = guild

    self._id = int(data['id'])

    self._load_variables(data)
    self.clear()
  
  def __repr__(self) -> str:
    return f'<{self.__class__.__name__} name={self._name!r} usable={self._usable} stack={self._stack}>'
  
  def _load_variables(self, data: TypeItem) -> None:
    if int(data['guild_id']) != self.guild.id:
      raise RuntimeError
    
    self._name = data['name']
    self._description = data['description']

    self._embed_title = data['embed_title']
    self._embed_description = data['embed_description']
    self._embed_image = data['embed_url']

    self._stack = data['stack']
    self._usable = data['usable']

    self._updated_at = datetime.fromtimestamp(data['updated_at'] / 1000) if data['updated_at'] is not None else None

  def clear(self) -> None:
    self._attacks: Dict[int, ItemAttack] = {  }

  def _get_http(self) -> HTTPClient:
    return self.state.http
  
  @property
  def attacks(self) -> List[ItemAttack]:
    return sorted(self._attacks.values(), key=lambda attack: attack._id)
  
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def id(self) -> int:
    return self._id
  
  @property
  def description(self) -> Union[str, None]:
    return self._description
  
  @property
  def embed_title(self) -> Union[str, None]:
    return self._embed_title

  @property
  def embed_description(self) -> Union[str, None]:
    return self._embed_description

  @property
  def embed_image(self) -> Union[str, None]:
    return self._embed_image
  
  @property
  def stack(self) -> int:
    return self._stack
  
  @property
  def usable(self) -> bool:
    return self._usable
  
  @property
  def updated_at(self) -> datetime:
    return self._updated_at
  
  @property
  def embeds(self) -> List[Embed]:
    return self.embed_at()

  def _get_attack_by_id(self, id: int) -> Union[ItemAttack, None]:
    return self._attacks.get(id)
  
  def _get_attack_by_name(self, name: str) -> Union[ItemAttack, None]:
    text_fmt = fmt

    name = text_fmt(name)
    attacks = self._attacks.values()

    return get(attacks, lambda attack: text_fmt(attack._name) == name)
  
  def get_attack(self, name_or_id: Union[str, int]) -> ItemAttack:
    result = self._get_attack_by_id(name_or_id) if isinstance(name_or_id, int) else self._get_attack_by_name(name_or_id)

    if result is None:
      raise geterr(ErrorType.ATTACK_NOTFOUND)
    
    return result
  
  async def create_attack(
    self,
    name:              str                 ,
    required_exp:      Optional[int] = None,
    damage:            Optional[int] = None,
    breath:            Optional[int] = None,
    blood:             Optional[int] = None,
    embed_title:       Optional[str] = None,
    embed_description: Optional[str] = None,
    embed_url:         Optional[str] = None
  ) -> ItemAttack:
    http = self._get_http()
    payload = { "name": name, "item_id": str(self._id) }

    if required_exp is not None:
      payload["required_exp"] = required_exp
    
    if damage is not None:
      payload["damage"] = damage
    
    if breath is not None:
      payload["breath"] = breath
    
    if blood is not None:
      payload["blood"] = blood
    
    if embed_title is not None:
      payload["embed_title"] = None

    if embed_description is not None:
      payload["embed_description"] = embed_description
    
    if embed_url is not None:
      payload["embed_url"] = embed_url

    data = await http.request(Route('POST', "/attacks/{gid}", gid=self.guild._id), json=payload)

    return ItemAttack(self.state, self, data)
  
  def _add_attack(self, attack: ItemAttack) -> None:
    self._attacks[attack.id] = attack
    self.guild._attacks[attack.id] = attack

  def _create_embed(
    self,
    start:       int, *,
    title:       Optional[str] = None,
    description: Optional[str] = None,
    url:         Optional[str] = None,
    
    cache:       Optional[List[ItemAttack]] = None
  ) -> Embed:
    if cache is None:
      cache = self.attacks

    chunk = (attack for attack in cache[start:start+self.LIMIT_PAGE] if attack._parent_id is None)

    cls = self.__class__
    ftx = format_text

    title = title or self._embed_title
    description = description or self._embed_description
    url = url or self._embed_image

    embed = Embed(
      title=ftx(title, name=self._name) if title is not None else self._name,
      description=ftx(description, name=self._name, description=self._description) if description is not None else cls.DEFAULT_DESCRIPTION
    )

    if url is not None:
      embed.set_image(url=url)
    embed.set_footer(text=cls.FOOTER_STYLE.format(self=self))
    embed.add_field(name='Attacks', value='**%s**' % '\n'.join(attack_format_discord(self.ATTACK_FORMATTER_STYLE, idx, attack, item=self) for (idx, attack) in enumerate(chunk, start=1)))

    return embed
  
  def embed_at(
    self, *,
    title:       Optional[str] = None,
    description: Optional[str] = None,
    url:         Optional[str] = None
  ) -> List[Embed]:
    attacks = self.attacks
    chunks = range(0, len(attacks), self.LIMIT_PAGE)
    embeds = [self._create_embed(chunk, title=title, description=description, url=url, cache=attacks) for chunk in chunks]

    return embeds

class PlayerItem:
  DEFAULT_AMOUNT: ClassVar[int] = 1

  def __init__(
    self,
    state: MorkatoConnectionState,
    player: Player,
    item: Item,
    data: TypePlayerItem
  ) -> None:
    self.state = state
    self.player = player
    self.item = item

    self.guild = player.guild

    if self.guild.id != self.item.guild.id:
      # Impossible block, but is prevent.
      
      raise RuntimeError("Algo deu errado, a guilda do player não é a mesma do item.")
    
    self._load_variables(data)
  
  def __repr__(self) -> str:
    return f'<PlayerItem player_name={self.player_name!r} item_name={self.item_name!r} player_id={self.player_id} item_id={self.item_id} amount={self._amount}>'
  
  def _load_variables(self, data: TypePlayerItem) -> None:
    guild_id = int(data['guild_id'])
    item_id = int(data['item_id'])
    player_id = int(data['player_id'])

    if (guild_id != self.guild.id or self.player.id != player_id or self.item.id != item_id):
      # Impossible block, but prevent.

      raise RuntimeError("Algo deu errado, as informações não são iguais.")
    
    self._amount = data['stack']
    self._created_at = datetime.fromtimestamp(data['created_at'] / 1000)

  @property
  def amount(self) -> int:
    return self._amount

  @property
  def item_name(self) -> str:
    return self.item._name
  
  @property
  def item_id(self) -> str:
    return self.item._id
  
  @property
  def item_description(self) -> Union[str, None]:
    return self.item._description
  
  @property
  def item_stack(self) -> int:
    return self.item._stack
  
  @property
  def item_usable(self) -> bool:
    return self.item._usable
  
  @property
  def player_name(self) -> int:
    return self.player._name
  
  @property
  def player_id(self) -> int:
    return self.player._id
  
  async def use(self, amount: Optional[int] = None) -> Self:
    amount = amount or self.DEFAULT_AMOUNT
    
    return await self.add(-abs(amount))
  
  async def add(self, amount: Optional[int] = None) -> Self:
    amount = amount or self.DEFAULT_AMOUNT
    
    raise NotImplementedError