import type { Express } from 'express'

import cors from 'cors'

export default (app: Express) => {
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
}