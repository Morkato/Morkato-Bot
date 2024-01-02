import type { Guild, GuildNotifyType, GuildDeleteFunction } from 'type:models/guild'
import type { Database } from 'type:models/database'

import { prismaError, errors } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { format } from 'utils/guild'

function geterr(err: any, { id }: { id: string }) {
  const type = prismaError(err)

  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](id);
  }

  return () => errors['generic.unknown']("Internal Error", "models/guild/delete");
}

export function deleteGuild(database: Database): GuildDeleteFunction {
  const session = database.session.guild

  return async ({ id }) => {
    id = assert(schemas.id, id)

    try {
      const prisma = await session.delete({
        where: { id }
      })

      const guild = format(prisma)

      database.notify<GuildNotifyType, Guild>({ type: 'guild.delete', data: guild })

      return guild;
    } catch (err) {
      const error = geterr(err, { id })

      throw error();
    }
  } // Function: Anonymous ({ id })
} // Function: deleteGuild

export default deleteGuild;