/**
 * infra/websocket;
 */

import { createServer } from 'http'

import object from 'utils/object'

import { Server, Socket } from 'socket.io'

type Client = Record<string, { sock: Socket, identify: string }>

declare global {
  let ws: Server | undefined
  let clients: Client
}

const events = {
  IDENTIFY(sock: Socket, { token }: any, clients: Client) {
    if(token && token === process.env.BOT_TOKEN) {
      clients[sock.id]['identify'] = token

      sock.emit('message', {
        e: 'READY',
        d: { token }
      })
    }
  }
}

function main() {
  const clients = {}

  const server = createServer((req, res) => {
    res.end()
  })

  const port = process.env.WEBSOCKET_PORT ? Number.parseInt(process.env.WEBSOCKET_PORT) : 8080

  global.ws = new Server(server)

  global.ws.on('connection', socket => {
    clients[socket.id] = { sock: socket, identify: null }

    console.log('New connection')

    socket.on('message', scope => {
      const { e, d } = scope
      
      const event = events[e]

      if(event) {
        event(socket, d, clients)
      }
    })
    
    socket.on('disconnect', () => {
      delete clients[socket.id]
    })
  })

  server.listen(port, () => {
    console.log('Connected websocket')
  })

  global.clients = clients
}

console.log(global)

if(!global.ws) {
  main()
}

export default global.ws;

function getFilteredClients(): Socket[] {
  return Object.values(object.filter(global.clients, ([key, value]) => value.identify === process.env.BOT_TOKEN))
}

export { getFilteredClients };