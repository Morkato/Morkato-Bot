import type { PlayerItemGetherFunction } from "type:models/playerItem"
import type { Database } from 'type:models/database'

import { prismaError, errors } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { format } from 'utils/playerItem'

function geterr(err: any) {
  return () => errors['generic.unknown']("Internal Error", "models/playerItem/get")
}

export function getPlayerItem(database: Database): PlayerItemGetherFunction {
  const session = database.session.playerItem

  return async ({ guild_id, player_id, item_id }) => {
    guild_id  = assert(schemas.id,  guild_id)
    player_id = assert(schemas.id, player_id)
    item_id   = assert(schemas.id,   item_id)

    try {
      const playerItem = await session.findUnique({
        where: { guild_id_player_id_item_id: { guild_id, player_id, item_id } }
      })

      if (!playerItem) {
        const error = errors["player-item.notfound"]

        throw error(guild_id, player_id, item_id);
      }

      return format(playerItem);
    } catch (err) {
      const error = geterr(err)

      throw error();
    }
  }
}