import type { PlayerItem, PlayerItemNotifyType, PlayerItemDeleteFunction } from 'type:models/playerItem'
import type { Database } from 'type:models/database'

import { prismaError, errors } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { format } from 'utils/playerItem'

function geterr(err: any, { gid, pid, iid }: { gid: string, pid: string, iid: string }) {
  const type = prismaError(err)
  
  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](gid);
  } else if (type === 'item.notfound') {
    return () => errors['item.notfound'](gid, iid);
  } else if (type === 'player.notfound') {
    return () => errors['player.notfound'](gid, pid);
  }
  
  return () => errors['generic.unknown']("Internal Error", "models/playerItem/edit");
}

export function deletePlayerItem(database: Database): PlayerItemDeleteFunction {
  const session = database.session.playerItem

  return async ({ guild_id, player_id, item_id }) => {
    guild_id  = assert(schemas.id,  guild_id)
    player_id = assert(schemas.id, player_id)
    item_id   = assert(schemas.id,   item_id)

    try {
      const prisma = await session.delete({
        where: { guild_id_player_id_item_id: { guild_id, player_id, item_id } }
      })

      const playerItem = format(prisma)

      database.notify<PlayerItemNotifyType, PlayerItem>({ type: 'player-item.delete', data: playerItem })

      return playerItem;
    } catch (err) {
      const error = geterr(err, { gid: guild_id, pid: player_id, iid: item_id })

      throw error();
    }
  } // Function: Anonymous ({ guild_id, player_id, item_id })
} // Function: deletePlayerItem

export default deletePlayerItem;