from __future__ import annotations

from typing import TYPE_CHECKING, List

from objects.types import guild, art, attack
from objects       import (
  Attack,
  Guild,
  Art
)

if TYPE_CHECKING:
  from .client import Morkato

import logging

_log = logging.getLogger(__name__)

async def create_guilds(client: Morkato, data: List[guild.Guild]) -> None:
  for guild in data:
    client.guilds.add(Guild(db=client, payload=guild))

async def create_arts(client: Morkato, data: List[art.Art]) -> None:
  for art in data:
    client.arts.add(Art(db=client, payload=art))

  _log.info(f'Loaded at +{len(client.arts)} arts from Gateway')

async def create_attacks(client: Morkato, data: List[attack.Attack]) -> None:
  for attack in data:
    client.attacks.add(Attack(db=client, payload=attack))

  _log.info(f'Loaded at +{len(client.attacks)} attacks from Gateway')

async def create_guild(client: Morkato, data: guild.Guild) -> None:
  client.guilds.add(Guild(db=client, payload=data))

async def create_art(client: Morkato, data: art.Art) -> None:
  client.arts.add(Art(db=client, payload=data))

async def create_attack(client: Morkato, data: attack.Attack) -> None:
  client.attacks.add(Attack(db=client, payload=data))

async def edit_art(client: Morkato, data: art.Art) -> None:
  guild = client.guilds.get(data['guild_id'])

  art = client.arts.get(guild=guild, name=data['name'])

  art._load_variables(data)

async def edit_attack(client: Morkato, data: attack.Attack) -> None:
  guild = client.guilds.get(data['guild_id'])

  attack = client.attacks.get(guild=guild, name=data['name'])

  attack._load_variables(data)

async def del_art(client: Morkato, data: art.Art) -> None:
  print('Deletou')
  
  client.arts.delete(guild_id=data['guild_id'], name=data['name'])

async def del_attack(client: Morkato, data: attack.Attack) -> None:
  client.attacks.delete(guild_id=data['guild_id'], name=data['name'])

events = [
  ('CREATE_GUILDS', create_guilds),
  ('CREATE_ARTS', create_arts),
  ('CREATE_ATTACKS', create_attacks),
  
  ('CREATE_GUILD', create_guild),
  ('CREATE_ART', create_art),
  ('CREATE_ATTACK', create_attack),

  ('DELETE_ART', del_art),
  ('DELETE_ATTACK', del_attack)
]