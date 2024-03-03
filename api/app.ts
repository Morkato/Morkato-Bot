import type { Logger } from 'type:logging'

import express from 'express'

import configureMiddlewares from 'extensions/middlewares'
import configureRoutes from 'extensions/router'
import configureCors from 'extensions/cors'

import { setupLogging } from 'morkato/logging'

import { getLogger } from 'logging'

export default () => {
  setupLogging(process.env.LOGGER_LEVELS ?? "debug,info,warning,error,critical")
  
  const logger = getLogger("morkato.app")
  const app = express()

  logger.debug("Starting Morkato APP")

  configureCors(app)
  configureMiddlewares(app)
  configureRoutes(app)
  
  return (func: (logger: Logger) => void) => {
    app.listen(5500, () => func(logger))

    return app;
  };
} 