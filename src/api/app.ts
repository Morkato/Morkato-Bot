import dotenv from 'dotenv'

import type { Request, Response, NextFunction } from 'express'
import type { WebSocketServer } from 'ws'

import { UnauthorizedError } from 'errors'

import { then } from './utils'

import Players from 'models/players'
import Attacks from 'models/attacks'
import Guilds  from 'models/guild'
import Arts    from 'models/arts'

import Guild  from './pages/guild'

import express from 'express'

import client from 'infra/database'

dotenv.config()

const players = Players(client.player)
const attacks = Attacks(client.attack)
const guilds  = Guilds(client.guild)
const arts    = Arts(client.art)

async function auth(req: Request, res: Response, next: NextFunction) {
  if (req.headers.authorization === process.env.BOT_TOKEN) {
    next()

    return;
  }

  throw new UnauthorizedError({ message: "Você não está autorizado para executar essa ação." })
}

export default (server: WebSocketServer) => {
  const app = express()

  app.use(express.json())
  
  app.use('/guilds', then(auth), Guild(server))

  server.on('connection', async sock => {
    sock.send(JSON.stringify({ e: 'HELLO', d: 'This device has connected of gateway!' }))

    sock.send(JSON.stringify({ e: 'CREATE_GUILDS', d: await guilds.getAll() }))
    sock.send(JSON.stringify({ e: 'CREATE_ARTS', d: await arts.where({}) }))
    sock.send(JSON.stringify({ e: 'CREATE_ATTACKS', d: await attacks.where({}) }))
    sock.send(JSON.stringify({ e: 'CREATE_PLAYERS', d: await players.where({}) }))

    sock.on('close', async code => {
      sock.close()
    })

  })
  
  return app;
};