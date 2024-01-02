import type { ArtWhereFunction } from "type:models/art"
import type { Database } from "type:models/database"

import { errors, prismaError } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { format } from 'utils/art'

export function whereArt(database: Database): ArtWhereFunction {
  const session = database.session.art
  
  return async ({ guild_id, type }) => {
    guild_id = guild_id ? assert(schemas.id, guild_id)   : undefined
    type     = type     ? assert(schemas.art_type, type) : undefined

    const arts = await session.findMany({
      where: { guild_id, type }
    })

    return arts.map(format);
  } // Function: Anonymous ({ guild_id, type })
} // Function: whereArt

export default whereArt;