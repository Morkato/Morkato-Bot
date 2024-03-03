/**
 * Route /arts/[guild_id]/[art_id]
 */

import type { Database } from 'type:models/database'

import { UnauthorizedError } from 'errors'
import { then } from 'utils/page'
import { Router } from 'express'

import routePostGuild from './post.guild'
import routeGetGuild from './get.guild'

import routeDeleteGuildArt from './delete.guild-art'
import routePutGuildArt from './put.guild-art'
import routeGetGuildArt from './get.guild-art'

export default (database: Database) => {
  const route = Router()

  route.use(then((req, res, next) => {
    if (!req.usr.roles.includes('MANAGE:ARTS')) {
      throw new UnauthorizedError({ type: 'generic.unknown' })
    }

    next()
  }))

  route.get('/:guild_id', then(routeGetGuild(database)))
  route.post('/:guild_id', then(routePostGuild(database)))

  route.get('/:guild_id/:art_id', then(routeGetGuildArt(database)))
  route.put('/:guild_id/:art_id', then(routePutGuildArt(database)))
  route.delete('/:guild_id/:art_id', then(routeDeleteGuildArt(database)))

  return route;
}