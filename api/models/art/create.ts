import type { PrismaClientKnownRequestError } from "@prisma/client/runtime/library"

import type { Art, ArtNotifyType, ArtCreateFunction, ArtCreateParameter } from "type:models/art"
import type { Database } from "type:models/database"

import { isArtUniqueByName, format } from 'utils/art'
import { assert, schemas } from 'utils/schema'
import { uuid } from 'utils/uuid'

import { errors, prismaError } from 'errors/prisma'
import { validate } from 'schemas'
import { whereArt } from './where'

export function geterr(err: PrismaClientKnownRequestError, guild_id: string) {
  const type = prismaError(err)

  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  }

  return () => errors['generic.unknown']("Internal Error", "models.art.create");
}

export function createArt(database: Database): ArtCreateFunction {
  const session = database.session.art

  const where = whereArt(database)

  return async ({ guild_id, data }) => {
    guild_id = assert(schemas.id, guild_id)

    const {
      name,
      type,
      
      exclude,

      embed_title,
      embed_description,
      embed_url
    } = validate(data, {
      name: 'required',
      art_type: 'required',

      exclude: 'optional',

      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional'
    }) as ArtCreateParameter['data']

    const arts = await where({ guild_id })

    if (!isArtUniqueByName({name, arts})) {
      const error = errors['art.alreadyexists']

      throw error(guild_id, name);
    }

    try {
      const prisma = await session.create({
        data: {
          guild_id: guild_id,
  
          name: name,
          type: type,
          id: uuid(),
  
          exclude: exclude ? 'true' : 'false',
  
          embed_title: embed_title,
          embed_description: embed_description,
          embed_url: embed_url
        }
      })

      const art = format(prisma)
      
      database.notify<ArtNotifyType, Art>({ type: 'art.create', data: art })

      return art;
    } catch (err) {
      const error = geterr(err, guild_id)

      throw error();
    }
  }
}

export default createArt;