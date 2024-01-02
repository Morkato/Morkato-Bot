from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  Optional,
  Sequence,
  Union,
  List
)

if TYPE_CHECKING:
  from typing_extensions import Self

  from .types.attack import Attack as TypeAttack
  
  from .state import MorkatoConnectionState
  from .http  import HTTPClient
  from .guild import Guild
  from .item  import Item
  from .art   import Art

from discord.embeds import Embed
from .http import Route
from .utils.etc import (
  format_text,
  num_fmt,
  find
)

from datetime import datetime

class Attack:
  def __init__(
    self,
    state: MorkatoConnectionState,
    guild: Guild,
    data: TypeAttack
  ) -> None:
    self.state = state
    self.guild = guild

    self._id = int(data['id'])

    self._load_variables(data)
  
  def __repr__(self) -> str:
    return f'<{self.__class__.__name__} name={self._name!r} id={self._id} state>'

  def _load_variables(self, data: TypeAttack) -> None:
    self._name = data['name']
    self._required_exp = data['required_exp']

    self._damage = data['damage']
    self._breath = data['breath']
    self._blood = data['blood']

    self._embed_title = data['embed_title']
    self._embed_description = data['embed_description']
    self._embed_image = data['embed_url']

    self._parent_id = int(data['parent_id']) if data['parent_id'] is not None else None
    
    self._updated_at = datetime.fromtimestamp(data['updated_at'] / 1000) if data['updated_at'] is not None else None
  
  def _get_http(self) -> HTTPClient:
    return self.state.http
  
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def id(self) -> int:
    return self._id
  
  @property
  def embed(self) -> Embed:
    return self.embed_at()
  
  @property
  def parent(self) -> Union[Attack, None]:
    if self._parent_id is None:
      return
    
    result = self.guild._get_attack_by_id(self._parent_id)
    
    return result
  
  @property
  def children(self) -> List[Attack]:
    def check(attack: Attack) -> bool:
      return attack._parent_id == self._id
    
    return sorted(find(self.guild._attacks.values(), check), key=lambda child: child._id)

  async def edit(
    self,
    name:              Optional[str] = None,
    required_exp:      Optional[int] = None,
    damage:            Optional[int] = None,
    breath:            Optional[int] = None,
    blood:             Optional[int] = None,
    embed_title:       Optional[str] = None,
    embed_description: Optional[str] = None,
    embed_url:         Optional[str] = None
  ) -> Self:
    http = self._get_http()
    payload = {  }

    if name is not None:
      payload["name"] = name

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

    if not payload:
      return self
    
    data = await http.request(Route('POST', '/attacks/{gid}/{aid}', gid=self.guild.id, aid=self._id), json=payload)
    self._load_variables(data)

    return self

  def embed_at(self, *,
    title:       Optional[str] = None,
    description: Optional[str] = None,
    url:         Optional[str] = None
  ) -> Embed:
    format  = format_text
    
    title       = title or self._embed_title
    description = description or self._embed_description
    url         = url or self._embed_image
    
    damage = num_fmt(self._damage, 2)
    breath = num_fmt(self._breath, 2)
    blood  = num_fmt(self._blood,  2)
    
    embed = Embed(
      title=format(title, name=self.name) if title else title,
      description=format(description,
        name=self.name,
        damage=damage,
        breath=breath,
        blood=blood
      ) if description else 'No description'
    )

    if url:
      embed.set_image(url=url)

    embed.set_footer(text=f'ID: {self.id}')

    return embed

class ArtAttack(Attack):
  def __init__(
    self,
    state: MorkatoConnectionState,
    art: Art,
    data: TypeAttack
  ) -> None:
    self.art = art

    super().__init__(state, art.guild, data)

  def _load_variables(self, data: TypeAttack) -> None:
    if int(data['art_id']) != self.art._id:
      raise RuntimeError
    
    return super()._load_variables(data)
  
  @property
  def parent(self) -> Union[ArtAttack, None]:
    if self._parent_id is None:
      return
    
    result = self.art._attacks.get(self._parent_id)
    
    return result
  
  @property
  def children(self) -> Sequence[ArtAttack]:
    def check(attack: ArtAttack) -> bool:
      return isinstance(attack, self.__class__) and attack._parent_id == self._id
    
    return sorted(find(self.art._attacks.values(), check), key=lambda child: child._id)

class ItemAttack(Attack):
  def __init__(
    self,
    state: MorkatoConnectionState,
    item: Item,
    data: TypeAttack
  ) -> None:
    self.item = item
    
    super().__init__(state, item.guild, data)

  def _load_variables(self, data: TypeAttack) -> None:
    if int(data['item_id']) != self.item._id:
      raise RuntimeError
  
    return super()._load_variables(data)
  
  @property
  def parent(self) -> Union[Attack, None]:
    if self._parent_id is None:
      return
    
    result = self.item._attacks.get(self._parent_id)
    
    return result
  
  @property
  def children(self) -> Sequence[ItemAttack]:
    def check(attack: ItemAttack) -> bool:
      return isinstance(attack, self.__class__) and attack._parent_id == self._id
    
    return sorted(find(self.item._attacks.values(), check), key=lambda child: child._id)