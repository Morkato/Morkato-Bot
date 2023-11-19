import type { Session } from 'morkato/gateway'
import type { WebSocketServer } from 'ws'

import { then, sender } from '../utils'
import { Router } from 'express'

import { WebSocketOP } from 'morkato/gateway/operators'
import { Events } from 'morkato/gateway/events'
import { filterClients } from 'morkato/gateway/etc'

import {
  players,
  player,
  forCreatePlayer,
  forEditPlayer,
  forDelPlayer
} from 'morkato/middleware/player'

export default (server: WebSocketServer, clients: Session[]) => {
  const route = Router()

  const jsonSender = sender('json')

  route.get('/:guild_id', then(players(jsonSender)))
  route.get('/:guild_id/:player_id', then(player(jsonSender)))

  route.post('/:guild_id', then(
    forCreatePlayer(async (req, res, next, player) => {
      res.json(player)

      filterClients(clients, 'MANAGE:PLAYERS').forEach(({ send }) => {
        send({ op: WebSocketOP.DISPATCH, e: Events.CREATE_PLAYER, d: player })
      })
    })
  ))

  route.post('/:guild_id/:player_id', then(
    forEditPlayer(async (req, res, next, { before, after }) => {
      res.json(after)

      filterClients(clients, 'MANAGE:PLAYERS').forEach(({ send }) => {
        send({ op: WebSocketOP.DISPATCH, e: Events.EDIT_PLAYER, d: { before, after } })
      })
    })
  ))

  route.delete('/:guild_id/:player_id', then(
    forDelPlayer(async (req, res, next, player) => {
      res.json(player)

      filterClients(clients, 'MANAGE:PLAYERS').forEach(({ send }) => {
        send({ op: WebSocketOP.DISPATCH, e: Events.DELETE_PLAYER, d: player })
      })
    })
  ))

  return route;
}