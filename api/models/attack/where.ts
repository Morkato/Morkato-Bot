import type { AttackWhereFunction } from "type:models/attack"
import type { Database } from "type:models/database"

import { assert, schemas } from 'utils/schema'
import { format } from "utils/attack"

export function whereAttack(database: Database): AttackWhereFunction {
  const session = database.session.attack

  return async ({ guild_id }) => {
    guild_id = guild_id ? assert(schemas.id, guild_id) : undefined

    const attacks = await session.findMany({
      where: { guild_id }
    })

    return attacks
      .map(prismaAttack => {
        const attack = format(prismaAttack)
        
        if (attack.parent_id !== null) {
          const parent =  attacks.find(p => p.id === attack.parent_id)
          if (!parent) {
            attack.parent_id = null
            return attack;
          }

          attack.art_id = parent.art_id
          attack.item_id = parent.item_id
        }

        return attack;
    });
  }
} // Function: whereAttack

export default whereAttack;