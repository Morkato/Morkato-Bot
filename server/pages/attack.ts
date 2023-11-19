import type { Session } from 'morkato/gateway'
import type { WebSocketServer } from 'ws'

import { then, sender } from '../utils'
import { Router } from 'express'

import { WebSocketOP } from 'morkato/gateway/operators'
import { Events } from 'morkato/gateway/events'
import { filterClients } from 'morkato/gateway/etc'

import {
  attacks,
  attack,
  forCreateAttack,
  forEditAttack,
  forDelAttack
} from 'morkato/middleware/attack'

export default (server: WebSocketServer, clients: Session[]) => {
  const route = Router()

  const jsonSender = sender('json')

  route.get('/:guild_id', then(attacks(jsonSender)))
  route.get('/:guild_id/:attack_id', then(attack(jsonSender)))

  route.post('/:guild_id', then(
    forCreateAttack(async (req, res, next, attack) => {
      filterClients(clients, 'MANAGE:ATTACKS').forEach(({ send }) => {
        send({ op: WebSocketOP.DISPATCH, e: Events.CREATE_ATTACK, d: attack })
      })

      res.json(attack)
    })
  ))

  route.post('/:guild_id/:attack_id', then(
    forEditAttack(async (req, res, next, { before, after }) => {
      filterClients(clients, 'MANAGE:ATTACKS').forEach(({ send }) => {
        send({ op: WebSocketOP.DISPATCH, e: Events.EDIT_ATTACK, d: { before, after } })
      })

      res.json(after)
    })
  ))

  route.delete('/:guild_id/:attack_id', then(
    forDelAttack(async (req, res, next, attack) => {
      filterClients(clients, 'MANAGE:ATTACKS').forEach(({ send }) => {
        send({ op: WebSocketOP.DISPATCH, e: Events.DELETE_ATTACK, d: attack })
      })

      res.json(attack)
    })
  ))

  return route;
}