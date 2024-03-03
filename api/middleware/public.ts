import type { Request, Response, NextFunction } from 'express'
import type { Logger } from 'type:logging'

import express from 'express'

export default (logger: Logger) => {
  return express.static(process.cwd() + '/public');
}