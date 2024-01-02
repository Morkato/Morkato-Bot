import type { Player, PlayerNotifyType, PlayerCreateFunction, PlayerCreateParameter } from 'type:models/player'
import type { Database } from 'type:models/database'

import { prismaError, errors } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { format } from 'utils/player'
import { validate } from 'schemas'

function geterr(err: any, { guild_id, id }: { guild_id: string, id: string }) {
  const type = prismaError(err)

  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  } else if (type === 'player.alreadyexists') {
    return () => errors['player.alreadyexists'](guild_id, id);
  }
  
  return () => errors['generic.unknown']("Internal Error", "models/player/create");
}

export function createPlayer(database: Database): PlayerCreateFunction {
  const session = database.session.player

  return async ({ guild_id, data }) => {
    guild_id = assert(schemas.id, guild_id)

    const {
      name,
      breed,
      id,

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
      name: 'required',
      breed: 'required',
      id: 'required',

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
    }) as PlayerCreateParameter['data']

    try {
      const prisma = await session.create({
        data: {
          guild_id: guild_id,
          name: name,
          breed: breed,
          id: id,

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

      const player = format(prisma)

      database.notify<PlayerNotifyType, Player>({ type: 'player.create', data: player })

      return player;
    } catch (err) {
      const error = geterr(err, { guild_id, id })

      throw error();
    }
  } // Function: ANonymous ({ guild_id, data })
} // Function: createPlayer

export default createPlayer;