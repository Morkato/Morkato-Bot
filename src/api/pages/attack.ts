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

  route.get('/:id/attacks', then(
    attacks(async (req, res, next, attacks) => {
      res.json(attacks)
    })
  ))

  route.post('/:id/attacks', then(
    forCreateAttack(async (req, res, next, attack) => {
      server.clients.forEach(sock => {
        sock.send(JSON.stringify({ e: 'CREATE_ATTACK', d: attack }))
      })
      
      res.json(attack)
    })
  ))

  route.get('/:id/attacks/:name', then(
    attack(async (req, res, next, attack) => {
      res.json(attack)
    })
  ))

  route.post('/:id/attacks/:name', then(
    forEditAttack(async (req, res, next, attack) => {
      server.clients.forEach(sock => {
        sock.send(JSON.stringify({ e: 'EDIT_ATTACK', d: attack }))
      })

      res.json(attack)
    })
  ))

  route.delete('/:id/attacks/:name', then(
    forDelAttack(async (req, res, next, attack) => {
      server.clients.forEach(sock => {
        sock.send(JSON.stringify({ e: 'DELETE_ATTACK', d: attack }))
      })

      res.json(attack)
    })
  ))
  
  return route;
}