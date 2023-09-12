from __future__ import annotations

from typing import TYPE_CHECKING, List

from .objects.types import guild, art, attack, player
from .objects       import (
  Player,
  Attack,
  Guild,
  Art
)

if TYPE_CHECKING:
  from .client import MorkatoClientManager

import logging

_log = logging.getLogger(__name__)

async def create_guilds(client: MorkatoClientManager, data: List[guild.Guild]) -> None:
  for guild in data:
    client.database.guilds.add(Guild(client=client, payload=guild))

async def create_arts(client: MorkatoClientManager, data: List[art.Art]) -> None:
  for art in data:
    client.database.arts.add(Art(db=client, payload=art))

  _log.info(f'Loaded at +{len(client.arts)} arts from Gateway')

async def create_attacks(client: MorkatoClientManager, data: List[attack.Attack]) -> None:
  for attack in data:
    client.database.attacks.add(Attack(client=client, payload=attack))

  _log.info(f'Loaded at +{len(client.attacks)} attacks from Gateway')

async def create_players(client: MorkatoClientManager, data: List[player.Player]) -> None:
  for player in data:
    client.database.players.add(Player(client=client, payload=player))

async def create_guild(client: MorkatoClientManager, data: guild.Guild) -> None:
  client.database.guilds.add(Guild(client=client, payload=data))

async def create_art(client: MorkatoClientManager, data: art.Art) -> None:
  art = Art(client=client, payload=data)

  client.database.arts.add(Art(client=client, payload=data))

  yml = f"```yml\nname: \"{art.name}\"\ntype: {art.type}\nguild_id: {art.guild_id}\nid: {art.id}```"

  await client.logs_channel.send(f'Foi criada uma nova arte (Informações úteis): {yml}\nJá sincronizei com meu banco de dados.')

async def create_attack(client: MorkatoClientManager, data: attack.Attack) -> None:
  client.database.attacks.add(Attack(client=client, payload=data))

async def edit_art(client: MorkatoClientManager, data: art.Art) -> None:
  art = client.database.arts.get(guild_id=data['guild_id'], id=data['id'])

  art._load_variables(data)

  yml = f"```yml\nname: \"{art.name}\"\ntype: {art.type}\nguild_id: {art.guild_id}\nid: {art.id}```"

  await client.logs_channel.send(f'Foi editada uma nova arte (Informações úteis): {yml}\nJá sincronizei com meu banco de dados.')

async def create_player(client: MorkatoClientManager, data: player.Player) -> None:
  client.database.players.add(Player(client=client, payload=data))

async def edit_attack(client: MorkatoClientManager, data: attack.Attack) -> None:
  attack = client.database.attacks.get(guild_id=data['guild_id'], id=data['id'])

  attack._load_variables(data)

async def del_art(client: MorkatoClientManager, data: art.Art) -> None:
  art = client.database.arts.delete(guild_id=data['guild_id'], id=data['id'])

  yml = f"```yml\nname: \"{art.name}\"\ntype: {art.type}\nguild_id: {art.guild_id}\nid: {art.id}```"

  await client.logs_channel.send(f'Foi deletado uma nova arte (Informações úteis): {yml}\nJá sincronizei com meu banco de dados.\nCriei um ponto de restauração.')

async def del_attack(client: MorkatoClientManager, data: attack.Attack) -> None:
  client.database.attacks.delete(guild_id=data['guild_id'], id=data['id'])

events = [
  ('CREATE_GUILDS', create_guilds),
  ('CREATE_ARTS', create_arts),
  ('CREATE_ATTACKS', create_attacks),
  ('CREATE_PLAYERS', create_players),
  
  ('CREATE_GUILD', create_guild),
  ('CREATE_ART', create_art),
  ('CREATE_ATTACK', create_attack),
  ('CREATE_PLAYER', create_player),

  ('DELETE_ART', del_art),
  ('DELETE_ATTACK', del_attack)
]