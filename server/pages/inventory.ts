import type { Session } from 'morkato/gateway'
import type { WebSocketServer } from 'ws'

import { then, sender } from '../utils'
import { Router } from 'express'

import { inventory } from 'morkato/middleware/inventory'

export default (server: WebSocketServer, clients: Session[]) => {
  const route = Router()

  const jsonSender = sender('json')

  route.get('/:guild_id/:player_id', then(inventory(jsonSender)))

  return route;
}