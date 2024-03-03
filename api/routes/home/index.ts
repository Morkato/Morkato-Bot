import type { Database } from 'type:models/database'

import { then } from 'utils/page'
import { Router } from 'express'

import routeGetMe from './get.me'

export default (database: Database) => {
  const route = Router()

  route.get('/', then(routeGetMe(database)))

  return route;
}