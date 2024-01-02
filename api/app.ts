import type { Session } from 'type:gateway/session'

import { prepareGatewaySubscriber } from 'models/gateway'
import { prepareWebSocketServer } from 'gateway/server'
import { prepareDatabase } from 'models/database'

import playerRouter from './pages/player'
import attackRouter from './pages/attack'
import guildRouter from './pages/guild'
import itemRouter from './pages/item'
import artRouter from './pages/art'

import express from 'express'
import auth from 'middleware/auth'
import cors from 'cors'

export default () => {
  const clients: Session[] = []

  const database = prepareDatabase()
  const gateway = prepareWebSocketServer(5550, database, clients)
  const subscriber = prepareGatewaySubscriber(clients)
  const app = express()

  app.use(express.json())
  app.use(auth())
  app.use(cors({
    origin: [ 'http://localhost:3000' ],
    methods: ["GET", "POST", "PUT", "DELETE"],
    allowedHeaders: [
      'Content-Type',
      'Content-Length',
      'Authorization',
      'X-Access-Control'
    ]
  }))

  app.use('/arts', artRouter(database))
  app.use('/items', itemRouter(database))
  app.use('/guilds', guildRouter(database))
  app.use('/attacks', attackRouter(database))
  app.use('/players', playerRouter(database))

  database.subscribe(subscriber)

  return app;
}