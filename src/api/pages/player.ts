import type { WebSocketServer } from 'ws'

import { then, send }   from '../utils'
import { Router } from 'express'

import {
  players,
  player,
  forCreatePlayer,
  forEditPlayer,
  forDelPlayer
} from 'api/middleware/player'



export default (server: WebSocketServer) => {
  const route = Router()

  route.get('/:guild_id/players', then(players(send('json'))))
  route.get('/:guild_id/players/:player_id', then(player(send('json'))))

  route.post('/:guild_id/players', then(
    forCreatePlayer(async (req, res, next, player) => {
      res.json(player)
      
      server.clients.forEach(sock => {
        sock.send(JSON.stringify({ e: 'CREATE_PLAYER', d: player }))
      })
    })
  ))

  route.post('/:guild_id/players/:player_id', then(
    forEditPlayer(async (req, res, next, player) => {
      res.json(player)

      server.clients.forEach(sock => {
        sock.send(JSON.stringify({ e: 'EDIT_PLAYER', d: player }))
      })
    })
  ))

  route.delete('/:guild_id/players/:player_id', then(
    forDelPlayer(async (req, res, next, player) => {
      res.json(player)

      server.clients.forEach(sock => {
        sock.send(JSON.stringify({ e: 'DELETE_PLAYER', d: player }))
      })
    })
  ))
  
  return route;
}