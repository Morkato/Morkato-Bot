import { createServer } from 'http'

import { WebSocketServer } from 'ws'
import make_app    from 'api/app'

const server = createServer((req, res) => {
  return app(req, res)
})
const io = new WebSocketServer({ server })

const app = make_app(io)

server.listen(80, () => console.log('server running...'))