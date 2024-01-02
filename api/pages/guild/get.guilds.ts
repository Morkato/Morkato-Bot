import type { GuildDatabase } from 'type:models/guild'
import type { Handler } from 'express'

export default function prepare(db: GuildDatabase): Handler {
  return async (req, res) => {
    const guilds = await db.where({  })

    return res.status(200).json(guilds);
  }
}