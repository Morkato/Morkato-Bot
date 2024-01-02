import type { IsUniqueAttackByNameParameter } from 'type:utils/attack'
import type { Attack as PrismaAttack } from '@prisma/client'
import type { Attack } from 'type:models/attack'

import { stripAll } from './string'

export function format({
  guild_id,

  name,
  id,

  art_id,
  item_id,
  parent_id,

  required_exp,

  damage,
  breath,
  blood,

  exclude,

  embed_title,
  embed_description,
  embed_url,

  updated_at
}: PrismaAttack): Attack {
  return {
    guild_id: guild_id,

    name: name,
    id: id,

    art_id: art_id,
    item_id: item_id,
    parent_id: parent_id,

    required_exp: required_exp,

    damage: damage,
    breath: breath,
    blood: blood,

    exclude: exclude === 'true',

    embed_title: embed_title,
    embed_description: embed_description,
    embed_url: embed_url,

    updated_at: updated_at === null ? null : Number(updated_at)
  }
}

export function isUniqueAttackByName({
  attacks,
  name,
  id,
  art_id,
  item_id,
  parent_id
}: IsUniqueAttackByNameParameter): boolean {
  name = stripAll(name)

  return attacks.find(other => other.id !== id && name === stripAll(other.name) && ((
    art_id
  ) || (
    item_id
    && item_id === other.item_id
  ) || (
    parent_id
  ))) === undefined;
}