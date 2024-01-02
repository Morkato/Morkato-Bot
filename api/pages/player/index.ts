/**
 * Route /players/[guild_id]/[player_id]
 */

import type { Database } from 'type:models/database'

import { UnauthorizedError } from 'errors'

import { preparePlayerDatabase } from 'models/player'
import { then } from 'utils/page'
import { Router } from 'express'

import routePostGuild from './post.guild'
import routeGetGuild from './get.guild'

import routeDeleteGuildPlayer from './delete.guild-player'
import routePostGuildPlayer from './post.guild-player'
import routeGetGuildPlayer from './get.guild-player'

export default (database: Database) => {
  const route = Router()

  const players = preparePlayerDatabase(database)

  route.use(then((req, res, next) => {
    if (!req.usr.roles.includes('MANAGE:PLAYERS')) {
      throw new UnauthorizedError({ type: 'generic.unknown' })
    }

    next()
  }))

  route.get('/:guild_id', then(routeGetGuild(players)))
  route.post('/:guild_id', then(routePostGuild(players)))

  route.get('/:guild_id/:player_id', then(routeGetGuildPlayer(players)))
  route.post('/:guild_id/:player_id', then(routePostGuildPlayer(players)))
  route.delete('/:guild_id/:player_id', then(routeDeleteGuildPlayer(players)))

  return route;
}