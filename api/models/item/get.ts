import type { ItemGetherFunction } from 'type:models/item'
import type { Database } from 'type:models/database'

import { assert, schemas } from 'utils/schema'
import { errors } from 'errors/prisma'
import { format } from 'utils/item'

export function getItem(database: Database): ItemGetherFunction {
  const session = database.session.item

  return async ({ guild_id, id }) => {
    guild_id = assert(schemas.id, guild_id)
    id       = assert(schemas.id,       id)

    const item = await session.findUnique({
      where: { guild_id_id: { guild_id, id } }
    })

    if (!item) {
      const error = errors['item.notfound']

      throw error(guild_id, id);
    }

    return format(item);
  } // Function: Anonymous ({ guild_id, id })
} // Function: getItem