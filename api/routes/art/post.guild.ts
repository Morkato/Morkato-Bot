import type { ArtDatabase } from 'type:models/art'
import type { Handler } from 'express'

import { extractGuildID } from 'utils/page'

export default function prepare(db: ArtDatabase): Handler {
  return async (req, res) => {
    const guild_id = extractGuildID(req)
    
    const art = await db.createArt({ guild_id, data: req.body })

    return res.status(201).json(art);
  }
}