import type { Database } from 'type:models/database'
import type { Session } from 'type:gateway/session'

import { WebSocketOperator } from 'type:gateway/operator'
import { createSession } from './session'
import { resolve } from 'utils/gateway'
import { WebSocketServer } from 'ws'

import { prepareDatabasePlayerItem } from 'models/playerItem'
import { preparePlayerDatabase } from 'models/player'
import { prepareDatabaseAttack } from 'models/attack'
import { prepareItemDatabase } from 'models/item'
import { prepareDatabaseGuild } from 'models/guild'
import { prepareDatabaseArt } from 'models/art'

import prepareHeartbeat from './heartbeat'

export function prepareWebSocketServer(port: number, database: Database, clients: Session[]): WebSocketServer {
  const server = new WebSocketServer({ port })

  const heartbeat = prepareHeartbeat(clients, 10000)

  const db = Object.freeze({
    base: database,
    guilds: prepareDatabaseGuild(database),
    arts: prepareDatabaseArt(database),
    players: preparePlayerDatabase(database),
    items: prepareItemDatabase(database),
    attacks: prepareDatabaseAttack(database),
    inventory: prepareDatabasePlayerItem(database)
  })

  server.on('connection', socket => {
    const session = createSession(socket)
    clients.push(session)

    socket.on('message', async stream => {
      const payload = resolve(stream.toString('utf-8'))
      
      if (!payload){
        return;
      }

      if (payload.op === WebSocketOperator.HEARTBEAT && payload.d) {
        session.setAlive(true)
        session.setLatency(Date.now() - Number(payload.d))
      } else if (payload.op === WebSocketOperator.IDENTIFY && payload.d) {
        session.setIdentify(payload.d['authorization'])

        const usr = session.getIdentify()

        if (!usr) {
          return;
        }

        if (usr.roles.includes('MANAGE:GUILDS')) {
          session.send({ op: WebSocketOperator.DISPATCH, e: 'RAW_CREATE_GUILD', d: await db.guilds.where({ }) })
        }

        if (usr.roles.includes('MANAGE:ARTS')) {
            session.send({ op: WebSocketOperator.DISPATCH, e: 'RAW_CREATE_ART', d: await db.arts.where({ }) })
        }

        if (usr.roles.includes('MANAGE:PLAYERS')) {
          session.send({ op: WebSocketOperator.DISPATCH, e: 'RAW_CREATE_PLAYER', d: await db.players.where({}) })
        }

        if (usr.roles.includes('MANAGE:ITEMS')) {
          session.send({ op: WebSocketOperator.DISPATCH, e: 'RAW_CREATE_ITEM', d: await db.items.where({}) })
        }

        if (usr.roles.includes('MANAGE:ATTACKS')) {
          session.send({ op: WebSocketOperator.DISPATCH, e: 'RAW_CREATE_ATTACK', d: await db.attacks.where({}) })
        }

        if (usr.roles.includes('MANAGE:PLAYER:ITEMS')) {
          session.send({ op: WebSocketOperator.DISPATCH, e: 'RAW_PLAYER_INVENTORY', d: await db.inventory.where({}) })
        }
      }
    })

    session.send({ op: WebSocketOperator.HELLO, d: "This device is connected with gateway!" })
  })

  return server;
}