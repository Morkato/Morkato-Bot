import type { Session } from 'morkato/gateway'
import type { WebSocketServer } from 'ws'

import { then, sender } from 'morkato/utils'
import { Router } from 'express'

import { WebSocketOP } from 'morkato/gateway/operators'
import { Events } from 'morkato/gateway/events'
import { filterClients } from 'morkato/gateway/etc'

import {
  items,
  item,
  forCreateItem,
  forEditItem,
  forDelItem
} from 'morkato/middleware/item'

export default (server: WebSocketServer, clients: Session[]) => {
  const route = Router()

  const jsonSender = sender('json')

  route.get('/:guild_id', then(items(jsonSender)))
  route.get('/:guild_id/:item_id', then(item(jsonSender)))

  route.post('/guild_id', then(forCreateItem(async (req, res, next, item) => {
    const promise = jsonSender(req, res, next, item)

    filterClients(clients, 'MANAGE:ITEMS').forEach(({ send }) => {
      send({ op: WebSocketOP.DISPATCH, e: Events.CREATE_ITEM, d: item })
    })

    await promise;
  })))

  route.post('/:guild_id/:item_id', then(forEditItem(async (req, res, next, { before, after }) => {
    const promise = jsonSender(req, res, next, after)

    filterClients(clients, 'MANAGE:ITEMS').forEach(({ send }) => {
      send({ op: WebSocketOP.DISPATCH, e: Events.EDIT_ITEM, d: { before, after } })
    })

    await promise;
  })))

  route.delete('/:guild_id/:item_id', then(forDelItem(async (req, res, next, item) => {
    const promise = jsonSender(req, res, next, item)

    filterClients(clients, 'MANAGE:ITEMS').forEach(({ send }) => {
      send({ op: WebSocketOP.DISPATCH, e: Events.DELETE_ITEM, d: item })
    })

    await promise;
  })))

  return route;
}

