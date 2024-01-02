import type { PrismaClientKnownRequestError } from "@prisma/client/runtime/library"

import type { Art, ArtNotifyType, ArtEditFunction, ArtEditParameter } from "type:models/art"
import type { Database } from "type:models/database"

import { isArtUniqueByName, format } from 'utils/art'
import { assert, schemas } from 'utils/schema'

import { errors, prismaError } from 'errors/prisma'
import { validate } from 'schemas'
import { whereArt } from './where'
import getArt from "./get"

export function geterr(err: PrismaClientKnownRequestError, guild_id: string, id: string, name?: string) {
  const type = prismaError(err)

  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  }

  return () => errors['generic.unknown']("Internal Error", "models.art.create");
}

export function editArt(database: Database): ArtEditFunction {
  const session = database.session.art

  const where = whereArt(database)
  const get   = getArt(database)

  return async ({ guild_id, id, data }) => {
    guild_id = assert(schemas.id, guild_id)
    id       = assert(schemas.id,       id)

    const {
      name,
      type,
      
      exclude,

      embed_title,
      embed_description,
      embed_url
    } = validate(data, {
      name: 'optional',
      art_type: 'optional',

      exclude: 'optional',

      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional'
    }) as ArtEditParameter['data']

    if (name && !isArtUniqueByName({ name, id, arts: await where({ guild_id }) })) {
      const error = errors['art.alreadyexists']

      throw error(guild_id, name);
    }

    const before = await get({ guild_id, id })

    try {
      const prisma = await session.update({
        where: { guild_id_id: { guild_id, id } },
        data: {
          name: name,
          type: type,

          exclude: exclude === undefined ? undefined : exclude ? 'true' : 'false',

          embed_title: embed_title,
          embed_description: embed_description,
          embed_url: embed_url,

          updated_at: Date.now()
        }
      })

      const after = format(prisma)

      database.notify<ArtNotifyType, { before: Art, after: Art }>({type: 'art.edit', data: { before, after }})
      
      return after;
    } catch (err) {
      const error = geterr(err, guild_id, id, name)

      throw error();
    }
  }
}

export default editArt;