import type { PlayerArtGetherFunction } from 'type:models/playerArt'
import type { Database } from 'type:models/database'

import { prismaError, errors } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { format } from 'utils/playerArt'

export function getPlayerArt(database: Database): PlayerArtGetherFunction {
  const session = database.session.playerArt

  return async ({ guild_id, player_id, art_id }) => {
    guild_id =  assert(schemas.id,  guild_id)
    player_id = assert(schemas.id, player_id)
    art_id =    assert(schemas.id,    art_id)

    try {
      const player = await session.create({
        data: {
          guild_id: guild_id,
          player_id: player_id,
          art_id: art_id,
          created_at: new Date()
        }
      })

      return format(player);
    } catch (err) {
      const type = prismaError(err)

      if (type === 'guild.notfound') {
        throw errors['guild.notfound'](guild_id);
      }

      throw errors['generic.unknown']("Unknown", "models.playerArt.create;")
    }
  }
}

export default getPlayerArt;