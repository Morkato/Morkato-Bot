import type { AttackDatabase } from 'type:models/attack'
import type { Handler } from 'express'

import { extractParam } from 'utils/page'

export default function prepare(db: AttackDatabase): Handler {
  return async (req, res) => {
    const guild_id = extractParam(req, 'guild_id')
    const attack_id = extractParam(req, 'attack_id')
    
    const attack = await db.delAttack({ guild_id, id: attack_id })

    return res.status(200).json(attack);
  }
}