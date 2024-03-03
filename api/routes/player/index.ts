/**
 * Route /players/[guild_id]/[player_id]
 */

import type { Database } from 'type:models/database'

import { UnauthorizedError } from 'errors'
import { then } from 'utils/page'
import { Router } from 'express'

import routePostGuild from './post.guild'
import routeGetGuild from './get.guild'

import routeDeleteGuildPlayer from './delete.guild-player'
import routePutGuildPlayer from './put.guild-player'
import routeGetGuildPlayer from './get.guild-player'

export default (database: Database) => {
  const route = Router()

  route.use(then((req, res, next) => {
    if (!req.usr.roles.includes('MANAGE:PLAYERS')) {
      throw new UnauthorizedError({ type: 'generic.unknown' })
    }

    next()
  }))

  route.get('/:guild_id', then(routeGetGuild(database)))
  route.post('/:guild_id', then(routePostGuild(database)))

  route.get('/:guild_id/:player_id', then(routeGetGuildPlayer(database)))
  route.put('/:guild_id/:player_id', then(routePutGuildPlayer(database)))
  route.delete('/:guild_id/:player_id', then(routeDeleteGuildPlayer(database)))

  return route;
}