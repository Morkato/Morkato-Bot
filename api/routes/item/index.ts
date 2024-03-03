/**
 * Route /items/[guild_id]/[player_id]
 */

import type { Database } from 'type:models/database'

import { UnauthorizedError } from 'errors'
import { then } from 'utils/page'
import { Router } from 'express'

import routePostGuild from './post.guild'
import routeGetGuild from './get.guild'

import routeDeleteGuildItem from './delete.guild-item'
import routePutGuildItem from './put.guild-item'
import routeGetGuildItem from './get.guild-item'

export default (database: Database) => {
  const route = Router()

  route.use(then((req, res, next) => {
    if (!req.usr.roles.includes('MANAGE:ITEMS')) {
      throw new UnauthorizedError({ type: 'generic.unknown' })
    }

    next()
  }))

  route.get('/:guild_id', then(routeGetGuild(database)))
  route.post('/:guild_id', then(routePostGuild(database)))

  route.get('/:guild_id/:item_id', then(routeGetGuildItem(database)))
  route.put('/:guild_id/:item_id', then(routePutGuildItem(database)))
  route.delete('/:guild_id/:item_id', then(routeDeleteGuildItem(database)))

  return route;
}