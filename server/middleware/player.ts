import type { Player } from 'models/players'
import type { Handler as ExpressHandler, Request } from 'express'
import type { Handler } from './types'

import { InternalServerError } from 'morkato/errors'

import { getGuildID } from './guild'

import client from 'morkato/infra/database'
import Players from 'models/players'

const {
  where,
  get,
  create,
  edit,
  del
} = Players(client.player, client.playerItem)

export function extractPlayerID(req: Request) {
  if (!req.params.player_id) {
    throw new InternalServerError({ message: "Erro interno no servidor" })
  }

  return req.params.player_id;
}

export function players(handle: Handler<Player[]>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)

    return await handle(req, res, next, await where({ guild_id }));
  }
}

export function player(handle: Handler<Player>): ExpressHandler {
  return async (req, res, next) => {
    const id = extractPlayerID(req)
    const guild_id = getGuildID(req)

    return await handle(req, res, next, await get({ guild_id, id }));
  }
}

export function forCreatePlayer(handle: Handler<Player>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)
    const id = req.body.id

    console.log(req.body)

    const player = await create({ guild_id, id, data: req.body })

    return await handle(req, res, next, player);
  }
}

export function forEditPlayer(handle: Handler<{ before: Player, after: Player }>): ExpressHandler {
  return async (req, res, next) => {
    const id = extractPlayerID(req)
    const guild_id = getGuildID(req)

    const before = await get({ guild_id, id })
    const player = await edit({ guild_id, id, data: req.body })

    return await handle(req, res, next, { before, after: player });
  }
}

export function forDelPlayer(handle: Handler<Player>): ExpressHandler {
  return async (req, res, next) => {
    const id = extractPlayerID(req)
    const guild_id = getGuildID(req)

    const player = await del({ guild_id, id })

    return await handle(req, res, next, player);
  }
}

export function forAddPlayerItem(handle: Handler<Player>): ExpressHandler {
  return async (req, res, next) => {
    const id = extractPlayerID(req)
    const guild_id = getGuildID(req)

    const { item_id, amount } = req.body

    const player = await add_item({ guild_id, id, item_id, amount })

    return await handle(req, res, next, player);
  }
}