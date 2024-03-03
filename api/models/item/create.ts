import type { Item, ItemNotifyType, ItemCreateFunction, ItemCreateParameter } from 'type:models/item'
import type { Database } from 'type:models/database'

import { format, isUniqueItemByName } from 'utils/item'
import { prismaError, errors } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { stripAll } from 'utils/string'
import { validate } from 'schemas'
import { uuid } from 'utils/uuid'

function geterr(type: string, guild_id: string) {
  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  }

  return () => errors['generic.unknown']("Internal Error", "models/item/create")
}

export function createItem(database: Database): ItemCreateFunction {
  const session = database.session.item

  return async ({ guild_id, data }) => {
    guild_id = assert(schemas.id, guild_id)

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
      name: 'required',
      description: 'optional',
      stack: 'optional',
      usable: 'optional',
      created_by: 'optional',
      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional'
    }) as ItemCreateParameter['data']

    if (!isUniqueItemByName({ name, items: await database.findItem({ guild_id }) })) {
      const error = errors['item.alreadyexists']

      throw error(guild_id, name);
    }

    let guildHasCreated = false
    
    async function execute() {
      try {
        const prisma = await session.create({
          data: {
            key: stripAll(name),
            guild_id: guild_id,
            id: uuid(),
  
            name: name,
            description: description,
  
            stack: stack,
            usable: usable ? 'true' : 'false',
            created_by: created_by,
            embed_title: embed_title,
            embed_description: embed_description,
            embed_url: embed_url
          }
        })
  
        const item = format(prisma)
  
        database.notify<ItemNotifyType, Item>({ type: 'item.create', data: item })
  
        return item;
      } catch (err) {
        const type = prismaError(err)

        if (type === 'guild.notfound' && !guildHasCreated) {
          await database.createGuild({ data: { id: guild_id } })
          guildHasCreated = true
          return await execute();
        }

        const error = geterr(type, guild_id)
  
        throw error();
      }
    }

    return await execute();
  } // Function: ANonymous ({ guild_id, data })
} // Function: createItem