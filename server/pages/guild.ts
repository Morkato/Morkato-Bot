import type { Session } from 'morkato/gateway'
import type { WebSocketServer } from 'ws'

import { then, sender } from 'morkato/utils'
import { Router } from 'express'

import { guild } from 'morkato/middleware/guild'

export default (server: WebSocketServer, clients: Session[]) => {
  const route = Router()

  const jsonSender = sender('json')

  route.get('/:guild_id', then(guild(jsonSender)))

  return route;
}