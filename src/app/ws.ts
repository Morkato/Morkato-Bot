import { WebSocketServer, WebSocket } from 'ws'
import { v4 as uuid } from 'uuid'

import object from 'utils/object'

type WS = WebSocketServer & {
  server: {
    clients: Record<string, { stream: WebSocket, identify: boolean }>
  }
}


type EventFunction<T extends any = any> = (ws: WS, { stream, id }: { stream: WebSocket, id: string }, d: T) => void

const events: Record<string, EventFunction | undefined> = {
  IDENTIFY(ws: WS, { stream, id }: Parameters<EventFunction>[1], d: Record<'token', string | undefined>) {
    if(d.token === process.env.BOT_TOKEN) {
      ws.server.clients[id]['identify'] = true  

      stream.send(JSON.stringify({
        e: 'READY',
        d
      }))
    }
  }
}

function main({ server }): WS {
  const ws: WS = Object.assign(new WebSocketServer({ server }), {
    server: server.server || {
      clients: server.server?.client || {}
    }
  })

  server.server = ws.server

  ws.on('connection', stream => {
    const id = uuid()

    ws.server.clients[id] = { stream, identify: false }

    stream.on('message', (data, isBinary) => {
      try {
        const { e, d } = JSON.parse(data.toString('utf-8'))

        const event = events[e]

        if(!event) {
          return;
        }

        event(ws, { stream, id }, d)
      } catch {  }
    })

    stream.on('close', index => {
      delete ws.server.clients[id]
    })
  })

  return ws;
}

export default main;

export function filterClients(props) {
  const ws = main(props)

  return Object.values(object.map(object.filter(ws.server.clients, ([key, value]) => value['identify']), ([key, value]) => value['stream']))
}