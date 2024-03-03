import type { Art, ArtNotifyType, ArtEditFunction, ArtEditParameter } from "type:models/art"
import type { Database, EditData } from "type:models/database"

import { assert, schemas } from 'utils/schema'
import { format } from 'utils/art'

import { errors, prismaError } from 'errors/prisma'
import { stripAll } from "utils/string"
import { validate } from 'schemas'

export function geterr(type: string, guild_id: string, id: string, name?: string) {
  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  } else if (type === 'art.notfound') {
    return () => errors['art.notfound'](guild_id, id);
  }

  return () => errors['generic.unknown']("Internal Error", "models.art.edit");
}

export function editArt(database: Database): ArtEditFunction {
  const session = database.session.art

  return async ({ guild_id, id, data }) => {
    guild_id = assert(schemas.id, guild_id)
    id       = assert(schemas.id,       id)

    const {
      name,
      type,
      
      exclude,
      created_by,

      embed_title,
      embed_description,
      embed_url
    } = validate(data, {
      name: 'optional',
      art_type: 'optional',

      exclude: 'optional',
      created_by: 'optional',

      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional'
    }) as ArtEditParameter['data']

    let key: string | undefined = undefined

    if (name) {
      key = stripAll(name)
    }

    const before: Art | undefined = database.observers.length === 0 ? undefined : await database.getArt({ guild_id, id })
    let guildHasCreated = false

    async function execute() {
      try {
        const prisma = await session.update({
          where: { guild_id_id: { guild_id, id } },
          data: {
            key: key,
            name: name,
            type: type,
  
            exclude: exclude === undefined ? undefined : exclude ? 'true' : 'false',
            created_by: created_by,
  
            embed_title: embed_title,
            embed_description: embed_description,
            embed_url: embed_url,
  
            updated_at: new Date()
          }
        })
  
        const after = format(prisma)
  
        if (before) {
          database.notify<ArtNotifyType, EditData<Art>>({type: 'art.edit', data: { before, after }})
        }
        
        return after;
      } catch (err) {
        const type = prismaError(err)
  
        if (type === 'guild.notfound' && !guildHasCreated) {
          await database.createGuild({ data: { id: guild_id } })
          guildHasCreated = true
          return await execute();
        }
  
        const error = geterr(type, guild_id, id, name)
  
        throw error();
      }
    }

    return await execute();
  }
}

export default editArt;