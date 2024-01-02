import type { AttackGetherFunction } from "type:models/attack"
import type { Database } from "type:models/database"

import { assert, schemas } from 'utils/schema'
import { errors } from "errors/prisma"
import { format } from "utils/attack"

export function getAttack(database: Database): AttackGetherFunction {
  const session = database.session.attack
  
  return async ({ guild_id, id }) => {
    guild_id = assert(schemas.id, guild_id)
    id       = assert(schemas.id,       id)

    const attack = await session.findUnique({
      where: { guild_id_id: { guild_id, id } }
    })

    if (!attack) {
      const error = errors['attack.notfound']

      throw error(guild_id, id);
    }

    return format(attack);
  } // Function: Anonymous ({ guild_id, id })
} // Function: getAttack

export default getAttack;