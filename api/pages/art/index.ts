/**
 * Route /arts/[guild_id]/[art_id]
 */

import type { Database } from 'type:models/database'

import { UnauthorizedError } from 'errors'

import { prepareDatabaseArt } from 'models/art'
import { then } from 'utils/page'
import { Router } from 'express'

import routePostGuild from './post.guild'
import routeGetGuild from './get.guild'

import routeDeleteGuildArt from './delete.guild-art'
import routePostGuildArt from './post.guild-art'
import routeGetGuildArt from './get.guild-art'

export default (database: Database) => {
  const route = Router()

  const arts = prepareDatabaseArt(database)

  route.use(then((req, res, next) => {
    if (!req.usr.roles.includes('MANAGE:ARTS')) {
      throw new UnauthorizedError({ type: 'generic.unknown' })
    }

    next()
  }))

  route.get('/:guild_id', then(routeGetGuild(arts)))
  route.post('/:guild_id', then(routePostGuild(arts)))

  route.get('/:guild_id/:art_id', then(routeGetGuildArt(arts)))
  route.post('/:guild_id/:art_id', then(routePostGuildArt(arts)))
  route.delete('/:guild_id/:art_id', then(routeDeleteGuildArt(arts)))

  return route;
}