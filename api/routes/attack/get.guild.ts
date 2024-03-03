import type { AttackDatabase } from 'type:models/attack'
import type { Handler } from 'express'

import { extractGuildID } from 'utils/page'

export default function prepare(db: AttackDatabase): Handler {
  return async (req, res) => {
    const guild_id = extractGuildID(req)
    
    const attacks = await db.findAttack({ guild_id })

    return res.status(200).json(attacks);
  }
}