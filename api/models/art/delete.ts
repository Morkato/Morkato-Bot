import type { Art, ArtDeleteFunction, ArtNotifyType } from "type:models/art"
import type { Database } from "type:models/database"

import { errors, prismaError } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { format } from 'utils/art'

export function geterr(type: string, guild_id: string, id: string) {
  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  } else if (type == 'art.notfound') {
    return () => errors['art.notfound'](guild_id, id);
  }

  return () => errors['generic.unknown']("Internal Error", "models.art.delete");
} // Function: geterr

export function deleteArt(database: Database): ArtDeleteFunction {
  const session = database.session.art

  return async ({ guild_id, id }) => {
    guild_id = assert(schemas.id, guild_id) as string
    id       = assert(schemas.id, id) as string

    try {
      const prisma = await session.delete({
        where: { guild_id_id: { guild_id, id } }
      })

      const art = format(prisma)

      database.notify<ArtNotifyType, Art>({ type: 'art.delete', data: art })

      return art;
    } catch (err) {
      const error = geterr(prismaError(err), guild_id, id)

      throw error();
    }
  } // Function: Anonymous ({ guild_id, id })
} // Function: deleteArt

export default deleteArt;