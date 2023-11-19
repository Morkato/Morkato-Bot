import type { Handler as ExpressHandler, Request } from 'express'
import type { Item } from 'models/items'
import type { Handler } from './types'

import { getGuildID } from './guild'

import { InternalServerError } from 'morkato/errors'

import client from 'morkato/infra/database'
import Items from 'models/items'

const {
  where,
  get,
  create,
  edit,
  del
} = Items(client.item)

export type HandlerItems = Handler<Item[]>
export type HandlerItem = Handler<Item>

export function extractItemID(req: Request) {
  if (!req.params.item_id) {
    throw new InternalServerError({ message: "Erro interno no servidor" })
  }

  return req.params.item_id;
}

export function item(handle: HandlerItem): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)
    const id = extractItemID(req)

    const item = await get({ guild_id, id })

    return await handle(req, res, next, item);
  }
}

export function items(handle: HandlerItems): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)

    const items = await where({ guild_id })

    return await handle(req, res, next, items);
  }
}

export function forCreateItem(handle: HandlerItem): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)

    const item = await create({ guild_id, data: req.body })

    return await handle(req, res, next, item);
  }
}

export function forEditItem(handle: Handler<{ before: Item, after: Item }>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)
    const id = extractItemID(req)

    const response = await edit({ guild_id, id, data: req.body })

    return await handle(req, res, next, response);
  }
}

export function forDelItem(handle: HandlerItem): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)
    const id = extractItemID(req)

    const item = await del({ guild_id, id })

    return await handle(req, res, next, item);
  }
}