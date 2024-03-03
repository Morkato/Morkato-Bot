import type { Player, PlayerNotifyType, PlayerEditFunction, PlayerEditParameter } from 'type:models/player'
import type { Database, EditData } from 'type:models/database'

import { prismaError, errors } from 'errors/prisma'
import { assert, schemas } from 'utils/schema'
import { format } from 'utils/player'
import { validate } from 'schemas'

function geterr(type: string, { guild_id, id }: { guild_id: string, id: string }) {
  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  } else if (type === 'player.notfound') {
    return () => errors['player.notfound'](guild_id, id);
  }
  
  return () => errors['generic.unknown']("Internal Error", "models/player/create");
}

export function editPlayer(database: Database): PlayerEditFunction {
  const session = database.session.player

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

    const before: Player | undefined = database.observers.length === 0 ? undefined : await database.getPlayer({ guild_id, id })
    let guildHasCreated = false
    
    async function execute() {
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
            banner: banner,

            updated_at: new Date()
          }
        })
  
        const after = format(prisma)
  
        if (before) {
          database.notify<PlayerNotifyType, EditData<Player>>({ type: 'player.edit', data: { before, after } })
        }
  
        return after;
      } catch (err) {
        const type = prismaError(err)
  
        if (type === 'generic.unknown' && !guildHasCreated) {
          await database.createGuild({ data: { id: guild_id } })
          guildHasCreated = true
          return await execute();
          
        }
  
        const error = geterr(type, { guild_id, id })
  
        throw error();
      }
    }

    return await execute();
  } // Function: Anonymous ({ guild_id, id, data })
} // Function: editPlayer

export default editPlayer;