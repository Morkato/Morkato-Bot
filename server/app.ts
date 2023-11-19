import dotenv from 'dotenv'

import type { Request, Response, NextFunction } from 'express'

import { UnauthorizedError } from 'morkato/errors'

import { WebSocketServer } from 'ws'
import { createServer } from 'http'

import { then } from './utils'

import Guild from './pages/guild'
import Player from './pages/player'
import Inventory from './pages/inventory'
import Attack from './pages/attack'
import Item from './pages/item'
import Art from './pages/arts'

import express from 'express'

import {
  WebSocketOP,
  Session,

  gatewaySettings,
  createSession,
  encode,
  ops
} from 'morkato/gateway'

dotenv.config()

async function auth(req: Request, res: Response, next: NextFunction) {
  if (req.headers.authorization === process.env.BOT_TOKEN) {
    next()

    return;
  }

  throw new UnauthorizedError({ message: "Você não está autorizado para executar essa ação." })
}

export default (port: number) => {
  const app = express()

  const io = new WebSocketServer({ port })

  const clients: Session[] = []

  app.use(express.json())

  app.use('/guilds', then(auth), Guild(io, clients))
  app.use('/attacks', then(auth), Attack(io, clients))
  app.use('/arts', then(auth), Art(io, clients))
  app.use('/players', then(auth), Player(io, clients))
  app.use('/items', then(auth), Item(io, clients))
  app.use('/inventory', then(auth), Inventory(io, clients))

  io.on('connection', async sock => {
    const session = createSession(sock)

    clients.push(session)

    sock.on('message', async (msg, isBinary) => {
      const payload = encode(msg.toString())

      const op = ops[payload.op]

      if (op) {
        await op(session, payload)
      }
    })

    session.send<string>({ op: WebSocketOP.HELLO, d: 'This device has connected of gateway!' })

    sock.on('close', async code => {
      session.terminate()
      session.setAlive(false)
    })
  })

  const interval = setInterval(() => {
    clients.filter(({ alive, terminate, ping, setAlive }) => {
      if (!alive) {
        terminate()

        return false;
      }

      setAlive(false)
      ping()

      return true;
    })
  }, gatewaySettings.HEARTBEAT_TICK)

  return {
    run(port: number) {
      const server = createServer(app)

      server.listen(port, () => console.log('server running...'))

      return server;
    },
    interval
  };
};