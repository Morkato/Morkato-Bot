import type { Player, PlayerNotifyType, PlayerDeleteFunction } from "type:models/player"
import type { Database } from 'type:models/database'

import { prismaError, errors } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { format } from 'utils/player'

function geterr(err: any, { guild_id, id }: { guild_id: string, id: string }) {
  const type = prismaError(err)

  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  } else if (type === 'player.notfound') {
    return () => errors['player.notfound'](guild_id, id);
  }
  
  return () => errors['generic.unknown']("Internal Error", "models/player/create");
}

export function deletePlayer(database: Database): PlayerDeleteFunction {
  const session = database.session.player

  return async ({ guild_id, id }) => {
    guild_id = assert(schemas.id, guild_id)
    id       = assert(schemas.id,       id)

    try {
      const prisma = await session.delete({
        where: { guild_id_id: { guild_id, id } }
      })

      const player = format(prisma)

      database.notify<PlayerNotifyType, Player>({ type: 'player.delete', data: player })

      return player;
    } catch (err) {
      const error = geterr(err, { guild_id, id })

      throw error();
    }
  } // Function: Anonymous ({ guild_id, id })
} // Function: deletePlayer

export default deletePlayer;