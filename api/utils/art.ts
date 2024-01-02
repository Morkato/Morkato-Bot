import type { IsUniqueArtByNameParameter } from 'type:utils/art'
import type { Art as PrismaArt } from '@prisma/client'
import type { Art } from 'type:models/art'

import { stripAll } from './string'

export function format({
  name,
  type,
  id,

  exclude,
  
  embed_title,
  embed_description,
  embed_url,

  guild_id,

  updated_at
}: PrismaArt): Art {
  return {
    name: name,
    type: type,
    id: id,

    exclude: exclude === 'true',

    embed_title: embed_title,
    embed_description: embed_description,
    embed_url: embed_url,

    guild_id: guild_id,

    updated_at: updated_at === null ? null : Number(updated_at)
  };
}

export function isArtUniqueByName({ name, id, arts }: IsUniqueArtByNameParameter) {
  name = stripAll(name)
  
  return arts.find(art => stripAll(art.name) === name && art.id !== id) === undefined;
}