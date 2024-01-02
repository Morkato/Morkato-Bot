import type { ArtGetherFunction } from 'type:models/art'
import type { Database } from 'type:models/database'

import { errors, prismaError } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { format } from 'utils/art'

export function getArt(database: Database): ArtGetherFunction {
  const session = database.session.art
  
  return async ({ guild_id, id }) => {
    guild_id = assert(schemas.id, guild_id) as string
    id       = assert(schemas.id, id) as string

    const art = await session.findUnique({
      where: { guild_id_id: { guild_id, id } }
    })

    if (!art) {
      const error = errors['art.notfound']

      throw error(guild_id, id);
    }

    return format(art);
  } // Function: Anonymous ({ guild_id, id })
} // Function: getArt

export default getArt;