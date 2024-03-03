import type { PlayerDatabase } from 'type:models/player'
import type { Handler } from 'express'

import { extractParam } from 'utils/page'

export default function prepare(db: PlayerDatabase): Handler {
  return async (req, res) => {
    const guild_id = extractParam(req, 'guild_id')
    const player_id = extractParam(req, 'player_id')
    
    const player = await db.getPlayer({ guild_id, id: player_id })

    return res.status(200).json(player);
  }
}