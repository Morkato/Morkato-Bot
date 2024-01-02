import type { PlayerItemWhereFunction } from "type:models/playerItem"
import type { Database } from "type:models/database"

import { assert, schemas } from 'utils/schema'
import { format } from 'utils/playerItem'

export function wherePlayerItem(database: Database): PlayerItemWhereFunction {
  const session = database.session.playerItem

  return async ({ guild_id, player_id, item_id }) => {
    guild_id  = guild_id  ? assert(schemas.id, guild_id)  : undefined
    player_id = player_id ? assert(schemas.id, player_id) : undefined
    item_id   = item_id   ? assert(schemas.id, item_id)   : undefined

    const playerItems = await session.findMany({
      where: { guild_id, player_id, item_id }
    })

    return playerItems.map(format);
  } // Function: Anonymous ({ guild_id, player_id, item_id })
} // Function: wherePlayerItem

export default wherePlayerItem;