import type { ItemDatabase } from 'type:models/item'
import type { Handler } from 'express'

import { extractParam } from 'utils/page'

export default function prepare(db: ItemDatabase): Handler {
  return async (req, res) => {
    const guild_id = extractParam(req, 'guild_id')
    
    const item = await db.createItem({ guild_id, data: req.body })

    return res.status(200).json(item);
  }
}