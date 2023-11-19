import type { PlayerItem } from 'models/player_items'
import type { Handler as ExpressHandler } from 'express'
import type { Handler } from './types'

import { extractPlayerID } from './player'
import { getGuildID } from './guild'

import Items from 'models/player_items'
import client from 'morkato/infra/database'

const {
  where
} = Items(client.playerItem)

export function inventory(handle: Handler<PlayerItem[]>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)
    const player_id = extractPlayerID(req)

    const inv = await where({ guild_id, player_id })

    return await handle(req, res, next, inv);
  }
}