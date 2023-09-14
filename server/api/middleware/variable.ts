import type { Handler as ExpressHandler, Request } from 'express'
import type { Variable } from 'models/variables'
import type { Handler } from '.'

import { InternalServerError } from 'errors'

import { getGuildID } from './guild'

import Variables from 'models/variables'

import client from 'infra/database'

const {
  get,
  getAll,
  create,
  edit,
  del
} = Variables(client.variable)

export function getVariableID(req: Request) {
  if (!req.params.name) {
    throw new InternalServerError({ message: "Erro interno no servidor" })
  }

  return req.params.name;
}

export function variables(handle: Handler<Variable[]>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)

    await handle(req, res, next, await getAll({ guild_id }))
  }
}

export function variable(handle: Handler<Variable>): ExpressHandler {
  return async (req, res, next) => {
    const name     = getVariableID(req)
    const guild_id = getGuildID(req)

    return await handle(req, res, next, await get({ guild_id, name }));
  }
}

export function forCreateVariable(handle: Handler<Variable>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)

    return await handle(req, res, next, await create({ guild_id, data: req.body }));
  }
}

export function forEditVariable(handle: Handler<{ before: Variable, after: Variable }>): ExpressHandler {
  return async (req, res, next) => {
    const name     = getVariableID(req)
    const guild_id = getGuildID(req)

    const before = await get({ guild_id, name })
    const after  = await edit({ guild_id, name, data: req.body })

    return await handle(req, res, next, { before: before, after: after });
  }
}

export function forDelVariable(handle: Handler<Variable>): ExpressHandler {
  return async (req, res, next) => {
    const name     = getVariableID(req)
    const guild_id = getGuildID(req)

    return await handle(req, res, next, await del({ guild_id, name }));
  }
}