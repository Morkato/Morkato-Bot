import type { ItemWhereFunction } from 'type:models/item'
import type { Database } from 'type:models/database'

import { assert, schemas } from 'utils/schema'
import { format } from 'utils/item'

export function whereItem(database: Database): ItemWhereFunction {
  const session = database.session.item

  return async ({ guild_id }) => {
    guild_id = guild_id ? assert(schemas.id, guild_id) : undefined

    const items = await session.findMany({
      where: { guild_id }
    })

    return items.map(format);
  } // Function: Anonymous ({ guild_id })
} // Function: whereItem

export default whereItem;