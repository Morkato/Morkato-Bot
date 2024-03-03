import type { Attack, AttackDeleteFunction, AttackNotifyType } from "type:models/attack"
import type { Database } from "type:models/database"

import { assert, schemas } from 'utils/schema'
import { prismaError, errors } from "errors/prisma"
import { format } from "utils/attack"

function geterr(err: unknown, { guild_id, id }: Pick<Attack, 'guild_id' | 'id'>) {
  const type = prismaError(err)

  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  } else if (type === 'attack.notfound') {
    return () => errors['attack.notfound'](guild_id, id);
  }

  return () => errors['generic.unknown']("Internal Error", "attack.create");
}

export function deleteAttack(database: Database): AttackDeleteFunction {
  const session = database.session.attack
  
  return async ({ guild_id, id }) => {
    guild_id = assert(schemas.id, guild_id)
    id       = assert(schemas.id,       id)

    try {
      const prisma = await session.delete({
        where: { guild_id_id: { guild_id, id } }
      })

      const attack = format(prisma)

      database.notify<AttackNotifyType, Attack>({ type: 'attack.delete', data: attack })

      return attack;
    } catch (err) {
      const error = geterr(err, { guild_id, id })

      throw error();
    }
  } // Function: Anonymous ({ guild_id, id })
} // Function: deleteAttack

export default deleteAttack;