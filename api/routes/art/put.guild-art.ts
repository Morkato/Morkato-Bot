import type { ArtDatabase } from 'type:models/art'
import type { Handler } from 'express'

import {
  extractGuildID,
  extractArtID
} from 'utils/page'

export default function prepare(db: ArtDatabase): Handler {
  return async (req, res) => {
    const guild_id = extractGuildID(req)
    const art_id   = extractArtID(req)
    
    const art = await db.editArt({ guild_id, id: art_id, data: req.body })

    return res.status(201).json(art);
  }
}