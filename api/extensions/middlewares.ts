import type { Express } from "express"

import { getLogger } from "logging"
import { json } from 'express'

import logging from 'middleware/logger'
import _public from 'middleware/public'
import auth from 'middleware/auth'

export default (app: Express) => {
  const logger = getLogger("morkato.server")

  app.use(json())
  app.use(auth())
  app.use(_public(logger))
  app.use(logging(logger))
}