/**
 * API PAGES Controller
 */

import type { Database } from 'type:models/database'
import type { Express } from 'express'

import auth from 'middleware/auth'

import playerRouter from './player'
import attackRouter from './attack'
import itemRouter from './item'
import artRouter from './art'

import express from 'express'
import cors from 'cors'

export function prepare(app: Express, database: Database): void {
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
  app.use
  app.use('/attacks', attackRouter(database))
}

export default prepare;