import type { WebSocketServer } from 'ws'

import { then }   from '../utils'
import { Router } from 'express'

import { guild } from '../middleware/guild'

import Variable from './variable'
import Player   from './player'
import Attack   from './attack'
import Art      from './arts'

export default (server: WebSocketServer) => {
  const route = Router()

  route.get('/:guild_id', then(
    guild(
      async (req, res, next, guild) => {
        res.json(guild)
      }
    )
  ))

  route.use('/', Variable(server))
  route.use('/', Player(server))
  route.use('/', Attack(server))
  route.use('/', Art(server))

  return route;
}