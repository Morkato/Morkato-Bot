import type { WebSocketServer } from 'ws'

import { then }   from '../utils'
import { Router } from 'express'

import {
  attacks,
  attack,
  forCreateAttack,
  forEditAttack,
  forDelAttack
} from 'api/middleware/attack'

export default (server: WebSocketServer) => {
  const route = Router()

  route.get('/:guild_id', then(
    attacks(async (req, res, next, attacks) => {
      res.json(attacks)
    })
  ))

  route.post('/:guild_id', then(
    forCreateAttack(async (req, res, next, attack) => {
      server.clients.forEach(sock => {
        sock.send(JSON.stringify({ e: 'CREATE_ATTACK', d: attack }))
      })
      
      res.json(attack)
    })
  ))

  route.get('/:guild_id/:attack_id', then(
    attack(async (req, res, next, attack) => {
      res.json(attack)
    })
  ))

  route.post('/:guild_id/:attack_id', then(
    forEditAttack(async (req, res, next, attack) => {
      server.clients.forEach(sock => {
        sock.send(JSON.stringify({ e: 'EDIT_ATTACK', d: attack }))
      })

      res.json(attack)
    })
  ))

  route.delete('/:guild_id/:attack_id', then(
    forDelAttack(async (req, res, next, attack) => {
      server.clients.forEach(sock => {
        sock.send(JSON.stringify({ e: 'DELETE_ATTACK', d: attack }))
      })

      res.json(attack)
    })
  ))
  
  return route;
}