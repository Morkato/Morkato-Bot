import type { PlayerGetherFunction } from "type:models/player"
import type { Database } from 'type:models/database'

import { assert, schemas } from 'utils/schema'
import { errors } from 'errors/prisma'
import { format } from 'utils/player'

export function getPlayer(database: Database): PlayerGetherFunction {
  const session = database.session.player

  return async ({ guild_id, id }) => {
    guild_id = assert(schemas.id, guild_id)
    id       = assert(schemas.id,       id)

    const player = await session.findUnique({
      where: { guild_id_id: { guild_id, id } }
    })

    if (!player) {
      const error = errors['player.notfound']

      throw error(guild_id, id);
    }
    
    return format(player);
  } // Function: Anonymous ({ guild_id, id })
} // Function: getPlayer

export default getPlayer;