import type { GuildGetherFunction } from "type:models/guild"
import type { Database } from "type:models/database"

import { assert, schemas } from 'utils/schema'
import { errors } from 'errors/prisma'
import { format } from 'utils/guild'

export function getGuild(database: Database): GuildGetherFunction {
  const session = database.session.guild

  return async ({ id }) => {
    id = assert(schemas.id, id)

    const guild = await session.findUnique({
      where: { id }
    })

    if (!guild) {
      const error = errors["guild.notfound"]

      throw error(id);
    }

    return format(guild);
  } // Function: Anonymous ({ id })
} // Function: getGuild

export default getGuild;