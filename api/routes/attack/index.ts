/**
 * Route /attacks/[guild_id]/[attack_id]
 */

import type { Database } from 'type:models/database'

import { UnauthorizedError } from 'errors'
import { then } from 'utils/page'
import { Router } from 'express'

import routePostGuild from './post.guild'
import routeGetGuild from './get.guild'

import routeDeleteGuildAttack from './delete.guild-attack'
import routePutGuildAttack from './put.guild-attack'
import routeGetGuildAttack from './get.guild-attack'

export default (database: Database) => {
  const route = Router()
  
  route.use(then((req, res, next) => {
    if (!req.usr.roles.includes('MANAGE:ATTACKS')) {
      throw new UnauthorizedError({ type: 'generic.unknown' })
    }

    next()
  }))
  
  route.get('/:guild_id', then(routeGetGuild(database)))
  route.post('/:guild_id', then(routePostGuild(database)))

  route.get('/:guild_id/:attack_id', then(routeGetGuildAttack(database)))
  route.put('/:guild_id/:attack_id', then(routePutGuildAttack(database)))
  route.delete('/:guild_id/:attack_id', then(routeDeleteGuildAttack(database)))

  return route;
}