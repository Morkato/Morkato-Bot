import type { IsUniqueAttackByNameParameter } from 'type:utils/attack'
import type { ArtType, Attack as PrismaAttack } from '@prisma/client'
import type { Attack } from 'type:models/attack'

import { stripAll } from './string'

export function format({
  guild_id,
  name,
  id,

  art_id,
  parent_id,

  title,
  description,
  banner,
  
  damage,
  breath,
  blood,

  exclude,
  intents,

  embed_title,
  embed_description,
  embed_url,

  created_by,
  updated_at
}: PrismaAttack): Attack {
  return {
    guild_id: guild_id,

    name: name,
    id: id,

    art_id: art_id,
    parent_id: parent_id,

    title: title,
    description: description,
    banner: banner,

    damage: damage,
    breath: breath,
    blood: blood,

    exclude: exclude === 'true',
    intents: intents,

    embed_title: embed_title,
    embed_description: embed_description,
    embed_url: embed_url,

    created_by: created_by,
    updated_at: updated_at === null ? null : updated_at.getTime()
  }
}

export function isUniqueAttackByName({
  attacks,
  name,
  id,
  art_id,
  is_fight_style,
  parent_id
}: IsUniqueAttackByNameParameter): boolean {
  name = stripAll(name)

  return attacks.find(other => other.id !== id && name === stripAll(other.name) && ((
    is_fight_style
    && other.art_id === art_id
  ) || art_id)) === undefined;
}