import type { ItemDatabase } from 'type:models/item'
import type { Handler } from 'express'

import { extractParam } from 'utils/page'

export default function prepare(db: ItemDatabase): Handler {
  return async (req, res) => {
    const guild_id = extractParam(req, 'guild_id')
    const item_id = extractParam(req, 'item_id')
    
    const item = await db.getItem({ guild_id, id: item_id })

    return res.status(200).json(item);
  }
}