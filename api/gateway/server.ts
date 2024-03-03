import type { Database } from 'type:models/database'
import type { Session } from 'type:gateway/session'

import { WebSocketOperator } from 'type:gateway/operator'
import { createSession } from './session'
import { resolve } from 'utils/gateway'
import { WebSocketServer } from 'ws'

import prepareHeartbeat from './heartbeat'

export function prepareWebSocketServer(port: number, database: Database, clients: Session[]): WebSocketServer {
  const server = new WebSocketServer({ port })

  const heartbeat = prepareHeartbeat(clients, 10000)

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

        if (usr.roles.includes('MANAGE:PLAYER:ARTS')) {
          session.send({
            op: WebSocketOperator.DISPATCH,
            e: 'RAW_PLAYER_ART',
            d: await database.findPlayerArt({})
          })
        }
      }
    })

    session.send({ op: WebSocketOperator.HELLO, d: "This device is connected with gateway!" })
  })

  return server;
}