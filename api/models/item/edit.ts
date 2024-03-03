import type { Item, ItemNotifyType, ItemEditFunction, ItemEditParameter } from 'type:models/item'
import type { Database, EditData } from "type:models/database"

import { prismaError, errors } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { stripAll } from 'utils/string'
import { format } from 'utils/item'
import { validate } from 'schemas'

function geterr(type: string, { guild_id, id }: Omit<ItemEditParameter, 'data'>) {
  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  } else if (type === 'item.notfound') {
    return () => errors['item.notfound'](guild_id, id);
  }

  return () => errors['generic.unknown']("Internal Error", "models/item/create");
}

export function editItem(database: Database): ItemEditFunction {
  const session = database.session.item

  return async ({ guild_id, id, data }) => {
    guild_id = assert(schemas.id, guild_id)
    id       = assert(schemas.id,       id)

    const {
      name,
      description,
      stack,
      usable,
      created_by,
      embed_title,
      embed_description,
      embed_url
    } = validate(data, {
      name: 'optional',
      description: 'optional',
      stack: 'optional',
      usable: 'optional',
      created_by: 'optional',
      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional'
    }) as ItemEditParameter['data']
    
    let key: string | undefined = name ? stripAll(name) : undefined

    const before: Item | undefined = database.observers.length === 0 ? undefined : await database.getItem({ guild_id, id })
    let guildHasCreated = false

    async function execute() {
      try {
        const prisma = await session.update({
          where: { guild_id_id: { guild_id, id } },
          data: {
            key: key,
            name: name,
            description: description,
            stack: stack,
            usable: usable === undefined ? undefined : usable ? 'true' : 'false',
            created_by: created_by,
            embed_title: embed_title,
            embed_description: embed_description,
            embed_url: embed_url
          }
        })
  
        const after = format(prisma)
  
        if (before) {
          database.notify<ItemNotifyType, EditData<Item>>({ type: 'item.edit', data: { before, after } })
        }
  
        return after;
      } catch (err) {
        const type = prismaError(err)
  
        if (type === 'guild.notfound' && !guildHasCreated) {
          await database.createGuild({ data: { id: guild_id } })
          guildHasCreated = true
          return await execute();
        }
        
        const error = geterr(type, { guild_id, id })
  
        throw error();
      }
    }

    return await execute();
  }
} // Function: editItem

export default editItem;