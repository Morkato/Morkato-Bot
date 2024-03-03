/**
 * [Extensions] Router configuration.
 */

import type { Session } from 'type:gateway/session'
import type { Express } from "express"

import { prepareGatewaySubscriber } from 'models/gateway'
import { prepareWebSocketServer } from 'gateway/server'
import { prepareDatabase } from 'models/database'

import { getLogger } from 'logging'

import playerRouter from 'routes/player'
import attackRouter from 'routes/attack'
import itemRouter from 'routes/item'
import artRouter from 'routes/art'
import meRouter from 'routes/home'

import notfound from 'notfound'

export default (app: Express) => {
  const logger = getLogger("morkato.router")
  const clients: Session[] = []

  const database = prepareDatabase()
  const gateway = prepareWebSocketServer(5550, database, clients)
  const subscriber = prepareGatewaySubscriber(clients)

  app.use('/me', meRouter(database))
  app.use('/arts', artRouter(database))
  app.use('/items', itemRouter(database))
  app.use('/attacks', attackRouter(database))
  app.use('/players', playerRouter(database))

  app.use('*', (req, res) => notfound(req, res))

  database.subscribe(subscriber)

  logger.debug("Routes has configured.")
}