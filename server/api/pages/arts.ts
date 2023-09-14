import type { WebSocketServer } from 'ws'

import { then }   from '../utils'
import { Router } from 'express'

import {
  arts,
  art,
  forCreateArt,
  forEditArt,
  forDelArt
} from 'api/middleware/art'

export default (server: WebSocketServer) => {
  const route = Router()

  route.get('/:guild_id', then(
    arts(async (req, res, next, arts) => {
      res.json(arts)
    })
  ))

  route.post('/:guild_id', then(
    forCreateArt(async (req, res, next, art) => {
      server.clients.forEach(client => {
        client.send(JSON.stringify({ 'e': 'CREATE_ART', d: art }))
      })
      
      res.json(art)
    })
  ))

  route.get('/:guild_id/:art_id', then(
    art(async (req, res, next, art) => {
      res.json(art)
    })
  ))

  route.post('/:guild_id/:art_id', then(
    forEditArt(async (req, res, next, { before, after }) => {
      server.clients.forEach(client => {
        client.send(JSON.stringify({ 'e': 'EDIT_ART', d: { before, after } }))
      })

      res.json(after)
    })
  ))

  route.delete('/:guild_id/:art_id', then(
    forDelArt(async (req, res, next, art) => {
      server.clients.forEach(client => {
        client.send(JSON.stringify({ 'e': 'DELETE_ART', d: art }))
      })

      res.json(art)
    })
  ))
  
  return route;
}