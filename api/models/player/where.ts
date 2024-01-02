import type { PlayerWhereFunction } from 'type:models/player'
import type { Database } from 'type:models/database'

import { assert, schemas } from 'utils/schema'
import { format } from 'utils/player'

export function wherePlayer(database: Database): PlayerWhereFunction {
  const session = database.session.player

  return async ({ guild_id }) => {
    guild_id = guild_id !== undefined ? assert(schemas.id, guild_id) : undefined

    const players = await session.findMany({
      where: { guild_id }
    })

    return players.map(format);
  } // Function: Anonymous ({ guild_id })
} // Function: wherePlayer

export default wherePlayer;