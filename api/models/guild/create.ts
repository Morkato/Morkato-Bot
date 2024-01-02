import type { Guild, GuildNotifyType, GuildCreateFunction, GuildCreateParameter } from 'type:models/guild'
import type { Database } from 'type:models/database'

import { prismaError, errors } from 'errors/prisma'
import { format } from 'utils/guild'
import { validate } from 'schemas'

function geterr(err: any, { id }: { id: string }) {
  const type = prismaError(err)

  if (type === 'guild.alreadyexists') {
    return () => errors['guild.alreadyexists'](id)
  }

  return () => errors['generic.unknown']("Internal Error", "models/guild/create");
}

export function createGuild(database: Database): GuildCreateFunction {
  const session = database.session.guild

  return async ({ data }) => {
    const { id } = validate(data, {
      id: 'required'
    }) as GuildCreateParameter['data']

    try {
      const prisma = await session.create({
        data: { id }
      })

      const guild = format(prisma)

      database.notify<GuildNotifyType, Guild>({ type: 'guild.create', data: guild })

      return guild;
    } catch (err) {
      const error = geterr(err, { id })

      throw error();
    }
  } // Function: Anonymous ({ data })
} // Function: createGuild

export default createGuild;