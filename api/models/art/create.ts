import type { Art, ArtNotifyType, ArtCreateFunction, ArtCreateParameter } from "type:models/art"
import type { Database } from "type:models/database"

import { isArtUniqueByName, format } from 'utils/art'
import { assert, schemas } from 'utils/schema'
import { uuid } from 'utils/uuid'

import { errors, prismaError } from 'errors/prisma'
import { stripAll } from "utils/string"
import { validate } from 'schemas'

export function geterr(type: string, guild_id: string) {  
  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  }

  return () => errors['generic.unknown']("Internal Error", "models.art.create");
}

export function createArt(database: Database): ArtCreateFunction {
  const session = database.session.art

  return async ({ guild_id, data }) => {
    guild_id = assert(schemas.id, guild_id)

    const {
      name,
      type,
      
      exclude,
      created_by,

      embed_title,
      embed_description,
      embed_url
    } = validate(data, {
      name: 'required',
      art_type: 'required',

      exclude: 'optional',
      created_by: 'optional',
      
      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional'
    }) as ArtCreateParameter['data']

    const arts = await database.findArt({ guild_id })

    if (!isArtUniqueByName({name, arts})) {
      const error = errors['art.alreadyexists']

      throw error(guild_id, name);
    }

    let guildHasCreated = false

    async function execute() {
      try {
        const prisma = await session.create({
          data: {
            guild_id: guild_id,
    
            key: stripAll(name),
            
            name: name,
            type: type,
            id: uuid(),
    
            exclude: exclude ? 'true' : 'false',
            created_by: created_by,
    
            embed_title: embed_title,
            embed_description: embed_description,
            embed_url: embed_url
          }
        })
  
        const art = format(prisma)
        
        database.notify<ArtNotifyType, Art>({ type: 'art.create', data: art })
  
        return art;
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
  }
}

export default createArt;