import type { IsUniqueItemByNameParameter } from 'type:utils/item'
import type { Item as PrismaItem } from '@prisma/client'
import type { Item } from 'type:models/item'

import { stripAll } from './string'

export function format({
  guild_id,
  id,
  name,
  description,
  stack,
  usable,
  embed_title,
  embed_description,
  embed_url,
  created_by,
  updated_at
}: PrismaItem): Item {
  return {
    guild_id: guild_id,
    id: id,

    name: name,
    description: description,
    stack: stack,
    usable: usable === 'true',
    embed_title: embed_title,
    embed_description: embed_description,
    embed_url: embed_url,

    created_by: created_by,
    updated_at: updated_at === null ? null : updated_at.getTime()
  }
}

export function isUniqueItemByName({ name, id, items }: IsUniqueItemByNameParameter): boolean {
  name = stripAll(name)
  
  return items.find(other => (
    stripAll(other.name) === name
    && other.id !== id
  )) === undefined;
}