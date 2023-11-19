import type { Session } from 'morkato/gateway'
import type { WebSocketServer } from 'ws'

import { then, sender } from '../utils'
import { Router } from 'express'

import { WebSocketOP } from 'morkato/gateway/operators'
import { Events } from 'morkato/gateway/events'
import { filterClients } from 'morkato/gateway/etc'

import {
  arts,
  art,
  forCreateArt,
  forEditArt,
  forDelArt
} from 'morkato/middleware/art'

export default (server: WebSocketServer, clients: Session[]) => {
  const route = Router()

  const jsonSender = sender('json')

  route.get('/:guild_id', then(arts(jsonSender)))
  route.get('/:guild_id/:art_id', then(art(jsonSender)))

  route.post('/:guild_id', then(
    forCreateArt(async (req, res, next, art) => {
      filterClients(clients, 'MANAGE:ARTS').forEach(({ send }) => {
        send({ op: WebSocketOP.DISPATCH, e: Events.CREATE_ART, d: art })
      })

      res.json(art)
    })
  ))

  route.post('/:guild_id/:art_id', then(
    forEditArt(async (req, res, next, { before, after }) => {
      filterClients(clients, 'MANAGE:ARTS').forEach(({ send }) => {
        send({ op: WebSocketOP.DISPATCH, e: Events.EDIT_ART, d: { before, after } })
      })

      res.json(after)
    })
  ))

  route.delete('/:guild_id/:art_id', then(
    forDelArt(async (req, res, next, art) => {
      filterClients(clients, 'MANAGE:ARTS').forEach(({ send }) => {
        send({ op: WebSocketOP.DISPATCH, e: Events.DELETE_ART, d: art })
      })

      res.json(art)
    })
  ))

  return route;
}