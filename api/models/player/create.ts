import type { Player, PlayerNotifyType, PlayerCreateFunction, PlayerCreateParameter } from 'type:models/player'
import type { Database } from 'type:models/database'

import { prismaError, errors } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { format } from 'utils/player'
import { validate } from 'schemas'

function geterr(type: string, { guild_id, id }: { guild_id: string, id: string }) {
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
      surname,
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
      surname: 'optional',
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

    let guildHasCreated = false
    
    async function execute() {
      try {
        const prisma = await session.create({
          data: {
            guild_id: guild_id,
            name: name,
            surname: surname,
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
        const type = prismaError(err)
  
        if (type === 'guild.notfound' && !guildHasCreated) {
          await database.createGuild({ data: { id: guild_id } })
          guildHasCreated = true
          return await execute();
        }
        
        const error = geterr(type, { guild_id, id })
  
        throw error();
      }
    }

    return await execute();
  } // Function: ANonymous ({ guild_id, data })
} // Function: createPlayer

export default createPlayer;