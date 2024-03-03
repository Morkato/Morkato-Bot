import type { PlayerItem, PlayerItemNotifyType, PlayerItemCreateFunction, PlayerItemCreateParameter } from 'type:models/playerItem'
import type { Database } from 'type:models/database'

import { prismaError, errors } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { format } from 'utils/playerItem'
import { validate } from 'schemas/index'

function geterr(err: any, { gid, pid, iid }: { gid: string, pid: string, iid: string }) {
  const type = prismaError(err)

  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](gid);
  } else if (type === 'item.notfound') {
    return () => errors['item.notfound'](gid, iid);
  } else if (type === 'player.notfound') {
    return () => errors['player.notfound'](gid, pid);
  }

  return () => errors['generic.unknown']("Internal Error", "models/playerItem/create");
}

export function createPlayerItem(database: Database): PlayerItemCreateFunction {
  const session = database.session.playerItem

  return async ({ guild_id, data }) => {
    guild_id = assert(schemas.id, guild_id)

    const {
      player_id,
      item_id,

      stack
    } = validate(data, {
      player_id: 'required',
      item_id:   'required',

      stack: 'optional'
    }) as PlayerItemCreateParameter['data']

    try {
      const prisma = await session.create({
        data: {
          guild_id: guild_id,
          player_id: player_id,
          item_id: item_id,

          stack: stack,

          created_at: new Date()
        }
      })

      const playerItem = format(prisma)

      database.notify<PlayerItemNotifyType, PlayerItem>({ type: 'player-item.create', data: playerItem })

      return playerItem;
    } catch (err) {
      const error = geterr(err, { gid: guild_id, pid: player_id, iid: item_id })

      throw error();
    }
  } // Function: Anonymous ({ guild_id, data })
} // Function: createPlayerItem

export default createPlayerItem;