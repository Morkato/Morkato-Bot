from __future__ import annotations

from decouple import config
from discord import Embed, Role

from .types.art import Art as TypedArt, Attack as TypedAttack
from requests import Response
from typing import Optional, Literal, TYPE_CHECKING
from unidecode import unidecode
from copy import deepcopy

from .string import format

import re

if TYPE_CHECKING:
  from .guild import Guild

LIMIT_PAGE = config('LIMIT_PAGE', 10) or 10
LIMIT_PAGE = int(LIMIT_PAGE)

def toKey(text: str) -> str:
  return unidecode(text).strip(' ').lower().replace(' ', '-')

class Attack:
  def __init__(self, payload: TypedAttack) -> None:
    
    self._load_variables(payload)
  
  def __repr__(self) -> str:
    return self.name

  def _load_variables(self, payload: TypedAttack) -> None:
    self.name = payload['name']
    
    self.roles_id = payload['roles']
    self.required_roles = payload['required_roles']

    self.damage = payload['damage']
    self.stamina = payload['stamina']

    self.embed_title = payload['embed_title']
    self.embed_description = payload['stamina']
    self.embed_url = payload['embed_url']

    self.fields = payload['fields']
  
  def in_message(self, message: str) -> bool:
    name = toKey(self.name.strip().replace(' ', '').replace('-', ''))
    
    return not not re.search("(( |-)+)?".join(letter for letter in name), message, re.IGNORECASE)

class Art:
  def __init__(self, guild: Guild, payload: TypedArt) -> None:
    self.guild = guild

    self._load_variables(payload)
  
  def _load_variables(self, data: TypedArt) -> None:
    self.name = data['name']
    self.type = data['type']
    self.role_id = data['role']

    self.embed_title = data['embed_title']
    self.embed_description = data['embed_description']
    self.embed_url = data['embed_url']

    self.attacks = self._load_attacks(data['attacks'])
  def _load_attacks(self, attacks: list[TypedAttack]) -> Attack:
    return [Attack(data) for data in attacks]
  
  def __repr__(self) -> str:
    return f'Respiration(guild={self.guild} name={self.name})'
  
  @property
  def embeds(self) -> list[Embed]:
    return self.embed_at()
  
  def embed_at(
    self, *,
    title: Optional[str] = None,
    description: Optional[str] = None,
    url: Optional[str] = None
  ) -> list[Embed]:
    title = title or self.embed_title or self.name
    description = format(description or self.embed_description, title=title) if description or self.embed_description else 'No description'
    url = self.embed_url

    embed = Embed(
      title=title,
      description=description
    )

    if url:
      embed.set_image(url=url)

    if not self.attacks:
      return [embed,]
    
    embeds = [ deepcopy(embed).add_field(name="Attacks", value='**%s**'%'\n'.join(f'{index} - {attack}' for index, attack in enumerate(self.attacks[i:i+LIMIT_PAGE], start=1))) for i in range(len(self.attacks))]

    return embeds
  
  def edit(
    self, *,
    name: Optional[str] = None,
    type: Optional[Literal['RESPIRATION', 'KEKKIJUTSU']] = None,
    role: Optional[Role] = None,

    embed_title: Optional[str] = None,
    embed_description: Optional[str] = None,
    embed_url: Optional[str] = None
  ) -> Art:
    def check(res: Response):
      if not res.status_code == 200:
        res.raise_for_status()
      
      return res.json()

    payload = {}

    if name:
      payload['name'] = name
    if type:
      payload['type'] = type
    if role:
      payload['role'] = str(role.id)
    if embed_title:
      payload['embed_title'] = embed_title
    if embed_description:
      payload['embed_description'] = embed_description
    if embed_url:
      payload['embed_url'] = embed_url

    data = self.guild.request_element('POST', f'/arts/{toKey(self.name)}', json=payload, call=check)

    self._load_variables(data)

    return self
  def delete(self) -> Art:
    def check(res: Response) -> TypedArt:
      if not res.status_code == 200:
        res.raise_for_status()

      return res.json()
    
    data = self.guild.request_element('DELETE', f'/arts/{toKey(self.name)}', call=check)

    self._load_variables(data)

    return self