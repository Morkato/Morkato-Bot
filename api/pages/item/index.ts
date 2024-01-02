/**
 * Route /items/[guild_id]/[player_id]
 */

import type { Database } from 'type:models/database'

import { UnauthorizedError } from 'errors'

import { prepareItemDatabase } from 'models/item'
import { then } from 'utils/page'
import { Router } from 'express'

import routePostGuild from './post.guild'
import routeGetGuild from './get.guild'

import routeDeleteGuildItem from './delete.guild-item'
import routePostGuildItem from './post.guild-item'
import routeGetGuildItem from './get.guild-item'

export default (database: Database) => {
  const route = Router()

  const items = prepareItemDatabase(database)

  route.use(then((req, res, next) => {
    if (!req.usr.roles.includes('MANAGE:ITEMS')) {
      throw new UnauthorizedError({ type: 'generic.unknown' })
    }

    next()
  }))

  route.get('/:guild_id', then(routeGetGuild(items)))
  route.post('/:guild_id', then(routePostGuild(items)))

  route.get('/:guild_id/:item_id', then(routeGetGuildItem(items)))
  route.post('/:guild_id/:item_id', then(routePostGuildItem(items)))
  route.delete('/:guild_id/:item_id', then(routeDeleteGuildItem(items)))

  return route;
}