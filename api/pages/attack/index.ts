/**
 * Route /attacks/[guild_id]/[attack_id]
 */

import type { Database } from 'type:models/database'

import { UnauthorizedError } from 'errors'

import { prepareDatabaseAttack } from 'models/attack'
import { then } from 'utils/page'
import { Router } from 'express'

import routePostGuild from './post.guild'
import routeGetGuild from './get.guild'

import routeDeleteGuildAttack from './delete.guild-attack'
import routePostGuildAttack from './post.guild-attack'
import routeGetGuildAttack from './get.guild-attack'

export default (database: Database) => {
  const route = Router()

  const attacks = prepareDatabaseAttack(database)

  route.use(then((req, res, next) => {
    if (!req.usr.roles.includes('MANAGE:ATTACKS')) {
      throw new UnauthorizedError({ type: 'generic.unknown' })
    }

    next()
  }))

  route.get('/:guild_id', then(routeGetGuild(attacks)))
  route.post('/:guild_id', then(routePostGuild(attacks)))

  route.get('/:guild_id/:attack_id', then(routeGetGuildAttack(attacks)))
  route.post('/:guild_id/:attack_id', then(routePostGuildAttack(attacks)))
  route.delete('/:guild_id/:attack_id', then(routeDeleteGuildAttack(attacks)))

  return route;
}