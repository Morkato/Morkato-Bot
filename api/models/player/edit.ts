import type { Player, PlayerNotifyType, PlayerEditFunction, PlayerEditParameter } from 'type:models/player'
import type { Database } from 'type:models/database'

import { prismaError, errors } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { format } from 'utils/player'
import { validate } from 'schemas'

import { getPlayer } from './get'

function geterr(err: any, { guild_id, id }: { guild_id: string, id: string }) {
  const type = prismaError(err)

  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  } else if (type === 'player.notfound') {
    return () => errors['player.notfound'](guild_id, id);
  }
  
  return () => errors['generic.unknown']("Internal Error", "models/player/create");
}

export function editPlayer(database: Database): PlayerEditFunction {
  const session = database.session.player

  const get = getPlayer(database)

  return async ({ guild_id, id, data }) => {
    guild_id = assert(schemas.id, guild_id)
    id       = assert(schemas.id,       id)

    const {
      name,
      breed,

      credibility,
      exp,
      cash,
      history,
      life,
      blood,
      breath,
      force,
      resistance,
      velocity,
      appearance,
      banner
    } = validate(data, {
      name: 'optional',
      breed: 'optional',

      credibility: 'optional',
      exp: 'optional',
      cash: 'optional',
      history: 'optional',
      life: 'optional',
      blood: 'optional',
      breath: 'optional',
      force: 'optional',
      resistance: 'optional',
      velocity: 'optional',
      appearance: 'optional',
      banner: 'optional'
    }) as PlayerEditParameter['data']

    const before = await get({ guild_id, id })
    
    try {
      const prisma = await session.update({
        where: { guild_id_id: { guild_id, id } },
        data: {
          name: name,
          breed: breed,

          credibility: credibility,
          exp: exp,
          cash: cash,
          history: history,
          life: life,
          blood: blood,
          breath: breath,
          force: force,
          resistance: resistance,
          velocity: velocity,
          appearance: appearance,
          banner: banner
        }
      })

      const after = format(prisma)

      database.notify<PlayerNotifyType, { before: Player, after: Player }>({ type: 'player.edit', data: { before, after } })

      return after;
    } catch (err) {
      const error = geterr(err, { guild_id, id })

      throw error();
    }
  } // Function: Anonymous ({ guild_id, id, data })
} // Function: editPlayer

export default editPlayer;