import type { Item, ItemNotifyType, ItemDeleteFunction, ItemDeleteParameter } from 'type:models/item'
import type { Database } from 'type:models/database'

import { prismaError, errors } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { format } from 'utils/item'

function geterr(err: any, { guild_id, id }: ItemDeleteParameter) {
  const type = prismaError(err)

  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  } else if (type == 'item.notfound') {
    return () => errors['item.notfound'](guild_id, id);
  }

  return () => errors['generic.unknown']("Internal Error", "models/item/delete");
}

export function deleteItem(database: Database): ItemDeleteFunction {
  const session = database.session.item

  return async ({ guild_id, id }) => {
    guild_id = assert(schemas.id, guild_id)
    id       = assert(schemas.id,       id)

    try {
      const prisma = await session.delete({
        where: { guild_id_id: { guild_id, id } }
      })

      const item = format(prisma)

      database.notify<ItemNotifyType, Item>({ type: 'item.delete', data: item })

      return item;
    } catch (err) {
      const error = geterr(err, { guild_id, id })

      throw error();
    }
  } // Function: Anonymous ({ guild_id, id })
} // Function: deleteItem

export default deleteItem;