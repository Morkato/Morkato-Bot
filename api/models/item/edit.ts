import type { Item, ItemNotifyType, ItemEditFunction, ItemEditParameter } from 'type:models/item'
import type { Database } from "type:models/database"

import { format, isUniqueItemByName } from 'utils/item'
import { prismaError, errors } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { validate } from 'schemas'

import { whereItem } from './where'
import { getItem } from './get'

function geterr(err: any, { guild_id, id }: Omit<ItemEditParameter, 'data'>) {
  const type = prismaError(err)

  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  } else if (type === 'item.notfound') {
    return () => errors['item.notfound'](guild_id, id);
  }

  return () => errors['generic.unknown']("Internal Error", "models/item/create");
}

export function editItem(database: Database): ItemEditFunction {
  const session = database.session.item

  const where = whereItem(database)
  const get   = getItem(database)

  return async ({ guild_id, id, data }) => {
    guild_id = assert(schemas.id, guild_id)
    id       = assert(schemas.id,       id)

    const {
      name,
      description,
      stack,
      usable,
      embed_title,
      embed_description,
      embed_url
    } = validate(data, {
      name: 'optional',
      description: 'optional',
      stack: 'optional',
      usable: 'optional',
      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional'
    }) as ItemEditParameter['data']
    
    if (name && !isUniqueItemByName({ name, id, items: await where({ guild_id })})) {
      const error = errors['item.alreadyexists']

      throw error(guild_id, name);
    }

    const before = await get({ guild_id, id })

    try {
      const prisma = await session.update({
        where: { guild_id_id: { guild_id, id } },
        data: {
          name: name,
          description: description,
          stack: stack,
          usable: usable === undefined ? undefined : usable ? 'true' : 'false',
          embed_title: embed_title,
          embed_description: embed_description,
          embed_url: embed_url
        }
      })

      const after = format(prisma)

      database.notify<ItemNotifyType, { before: Item, after: Item }>({ type: 'item.edit', data: { before, after } })

      return after;
    } catch (err) {
      const error = geterr(err, { guild_id, id })

      throw error();
    }
  }
} // Function: editItem

export default editItem;