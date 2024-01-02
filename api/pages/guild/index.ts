/**
 * Route /guilds/[guild_id]/[art_id]
 */

import type { Database } from 'type:models/database'

import { UnauthorizedError } from 'errors'

import { prepareDatabaseGuild } from 'models/guild'
import { then } from 'utils/page'
import { Router } from 'express'

import routeGetGuilds from './get.guilds'

export default (database: Database) => {
  const route = Router()

  const guilds = prepareDatabaseGuild(database)

  route.use(then((req, res, next) => {
    if (!req.usr.roles.includes('MANAGE:ARTS')) {
      throw new UnauthorizedError({ type: 'generic.unknown' })
    }

    next()
  }))

  route.get('/', then(routeGetGuilds(guilds)))

  return route;
}