from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  Optional,
  ClassVar,
  Union,
  Dict,
  List
)

if TYPE_CHECKING:
  from typing_extensions import Self
  from .types.art import Art as TypeArt, ArtType
  
  from .state import MorkatoConnectionState
  from .http  import HTTPClient
  from .guild import Guild

from .utils.etc import attack_format_discord, format_text
from .errors import ErrorType, geterr
from discord.embeds import Embed
from datetime import datetime
from .attack import ArtAttack
from .http import Route

class Art:
  RESPIRATION: ClassVar[ArtType] = 'RESPIRATION'
  KEKKIJUTSU: ClassVar[ArtType] = 'KEKKIJUTSU'
  FIGHTING_STYLE: ClassVar[ArtType] = 'FIGHTING_STYLE'

  LIMIT_PAGE: ClassVar[int] = 10

  DEFAULT_DESCRIPTION: ClassVar[str] = "No description"
  FOOTER_STYLE: ClassVar[str] = "ID: {self.id}"
  ATTACK_FORMATTER_STYLE: ClassVar[str] = "{index}° - !a `{attack.name}`"

  def __init__(
    self,
    state: MorkatoConnectionState,
    guild: Guild,
    data: TypeArt
  ) -> None:
    self.state = state
    self.guild = guild

    self._load_variables(data)
    self.clear()
  
  def _load_variables(self, data: TypeArt) -> None:
    guild_id = int(data['guild_id'])

    if guild_id != self.guild.id:
      raise RuntimeError # Impossible error, but is prevent
    
    self._id = int(data['id'])

    self._name = data['name']
    self._type = data['type']
    self._id   = int(data['id'])

    self._exclude = data['exclude']

    self._title       = data['embed_title']
    self._description = data['embed_description']
    self._image_url   = data['embed_url']

    self._updated_at = datetime.fromtimestamp(data['updated_at'] / 1000) if data['updated_at'] is not None else None

  def __repr__(self) -> str:
    cls = self.__class__
    type = 'Respiration' if self.type == cls.RESPIRATION else 'Kekkijutsu' if self.type == cls.KEKKIJUTSU else 'FightStyle'
    
    return f'<Art.{type} name={self._name!r}>'
  
  def clear(self) -> None:
    self._attacks: Dict[str, ArtAttack] = {  }
  
  def _add_attack(self, attack: ArtAttack) -> None:
    self._attacks[attack.id] = attack
    self.guild._attacks[attack.id] = attack
  
  @property
  def attacks(self) -> List[ArtAttack]:
    return sorted(self._attacks.values(), key=lambda attack: attack._id)
  
  @property
  def id(self) -> int:
    return self._id
  
  @property
  def name(self) -> str:
    return self._name
  
  @property
  def type(self) -> ArtType:
    return self._type
  
  @property
  def title(self) -> Union[str, None]:
    return self._title
  
  @property
  def description(self) -> Union[str, None]:
    return self._description
  
  @property
  def image_url(self) -> Union[str, None]:
    return self._image_url
  
  @property
  def embeds(self) -> List[Embed]:
    return self.embed_at()

  def _get_http(self) -> HTTPClient:
    return self.state.http
  
  def _get_attack_by_id(self, id: int) -> Union[ArtAttack, None]:
    return self._attacks.get(id)
  
  def get_attack(self, name_or_id: Union[str, int]) -> ArtAttack:
    if isinstance(name_or_id, str):
      raise NotImplemented
    
    result = self._get_attack_by_id(name_or_id)

    if result is None:
      raise geterr(ErrorType.ATTACK_NOTFOUND)
    
    return result
  
  async def edit(
    self, *,
    name: Optional[str]              = None,
    type: Optional[ArtType]          = None,
    embed_title: Optional[str]       = None,
    embed_description: Optional[str] = None,
    embed_url: Optional[str]         = None
  ) -> Self:
    http = self._get_http()

    payload = {  }

    if name is not None:
      payload['name'] = name
    
    if type is not None:
      payload['type'] = type
    
    if embed_title is not None:
      payload['embed_title'] = embed_title
    
    if embed_description is not None:
      payload['embed_description'] = embed_description
    
    if embed_url is not None:
      payload['embed_url'] = embed_url
    
    if not payload:
      return self
    
    data = await http.request(Route('POST', '/arts/{gid}/{id}', gid=self.guild.id, id=self._id), json=payload)

    self._load_variables(data)

    return self

  async def delete(self) -> Self:
    http = self._get_http()

    data = await http.request(Route('DELETE', '/arts/{gid}/{id}', gid=self.guild.id, id=self._id))

    self._load_variables(data)

    return self

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
  ) -> ArtAttack:
    http = self._get_http()
    payload = { "name": name, "art_id": str(self._id) }

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

    return ArtAttack(self.state, self, data)

  def _create_embed(
    self,
    start:       int, *,
    title:       Optional[str] = None,
    description: Optional[str] = None,
    url:         Optional[str] = None,
    
    cache:       Optional[List[ArtAttack]] = None
  ) -> Embed:
    if cache is None:
      cache = self.attacks

    chunk = (attack for attack in cache[start:start+self.LIMIT_PAGE] if attack._parent_id is None)

    cls = self.__class__
    ftx = format_text

    title = title or self._title
    description = description or self._description
    url = url or self._image_url

    embed = Embed(
      title=ftx(title, name=self._name) if title is not None else self._name,
      description=ftx(description, name=self._name) if description is not None else cls.DEFAULT_DESCRIPTION
    )

    if url is not None:
      embed.set_image(url=url)
    embed.set_footer(text=cls.FOOTER_STYLE.format(self=self))
    embed.add_field(name='Attacks', value='**%s**' % '\n'.join(attack_format_discord(self.ATTACK_FORMATTER_STYLE, idx, attack) for (idx, attack) in enumerate(chunk, start=1)))

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