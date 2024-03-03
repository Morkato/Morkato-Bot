import type { PlayerItem, PlayerItemNotifyType, PlayerItemEditFunction, PlayerItemEditParameter } from 'type:models/playerItem'
import type { Database, EditData } from 'type:models/database'

import { prismaError, errors } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { format } from 'utils/playerItem'
import { validate } from 'schemas'

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

export function editPlayerItem(database: Database): PlayerItemEditFunction {
  const session = database.session.playerItem

  return async ({ guild_id, player_id, item_id, data }) => {
    guild_id  = assert(schemas.id,  guild_id)
    player_id = assert(schemas.id, player_id)
    item_id   = assert(schemas.id,   item_id)

    const { stack } = validate(data, {
      stack: 'optional'
    }) as PlayerItemEditParameter['data']

    const before = await database.getPlayerItem({ guild_id, player_id, item_id })

    try {
      const prisma = await session.update({
        where: { guild_id_player_id_item_id: { guild_id, player_id, item_id } },
        data: { stack }
      })

      const after = format(prisma)

      database.notify<PlayerItemNotifyType, EditData<PlayerItem>>({ type: 'player-item.edit', data: { before, after } })

      return after;
    } catch (err) {
      const error = geterr(err, { gid: guild_id, pid: player_id, iid: item_id })

      throw error();
    }
  } // Function: Anonymous ({ guild_id, player_id, item_id, data })
} // Function: editPlayerFunction

export default editPlayerItem;