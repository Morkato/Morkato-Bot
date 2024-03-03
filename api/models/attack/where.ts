import type { AttackWhereFunction } from "type:models/attack"
import type { Database } from "type:models/database"

import { assert, schemas } from 'utils/schema'
import { format } from "utils/attack"

export function whereAttack(database: Database): AttackWhereFunction {
  const session = database.session.attack

  return async ({ guild_id, art_id }) => {
    guild_id = guild_id ? assert(schemas.id, guild_id) : undefined

    const attacks = await session.findMany({
      where: { guild_id, art_id }
    })

    return attacks
      .map(format);
  }
} // Function: whereAttack

export default whereAttack;