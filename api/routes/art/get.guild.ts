import type { ArtDatabase } from 'type:models/art'
import type { Handler } from 'express'

import { extractGuildID } from 'utils/page'

export default function prepare(database: ArtDatabase): Handler {
  return async (req, res) => {
    const guild_id = extractGuildID(req)
    
    const arts = await database.findArt({ guild_id })

    return res.status(200).json(arts);
  }
}