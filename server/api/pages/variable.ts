import type { WebSocketServer } from 'ws'

import { then }   from '../utils'
import { Router } from 'express'

import { 
  variables,
  variable,
  forCreateVariable,
  forEditVariable,
  forDelVariable
} from 'api/middleware/variable'

export default (server: WebSocketServer) => {
  const route = Router()

  route.get('/:id/variables', then(
    variables(async (req, res, next, variables) => {
      res.json(variables)
    })
  ))

  route.post('/:id/variables', then(
    forCreateVariable(async (req, res, next, variable) => {
      res.json(variable)
    })
  ))

  route.get('/:id/variables/:name', then(
    variable(async (req, res, next, variable) => {
      res.json(variable)
    })
  ))

  route.post('/:id/variables/:name', then(
    forEditVariable(async (req, res, next, { after, before }) => {
      res.json(after)
    })
  ))

  route.delete('/:id/variables/:name', then(
    forDelVariable(async (req, res, next, variable) => {
      res.json(variable)
    })
  ))
  
  return route;
}