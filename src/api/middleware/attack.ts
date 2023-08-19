import type { Handler as ExpressHandler, Request } from 'express'
import type { Attack } from 'models/attacks'
import type { Handler } from '.'

import { InternalServerError } from 'errors'

import { getGuildID } from './guild'

import Attacks from 'models/attacks'

import client from 'infra/database'

const {
  where,
  get,
  create,
  edit,
  del
} = Attacks(client.attack)

export function getAttackID(req: Request) {
  if (!req.params.name) {
    throw new InternalServerError({ message: "Erro interno no servidor" })
  }

  return req.params.name;
}

export function attack(handle: Handler<Attack>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)
    const id       = getAttackID(req)

    return await handle(req, res, next, await get({ guild_id, id }));
  }
}

export function attacks(handle: Handler<Attack[]>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)
    const art_id   = !req.query.art_name ? undefined : req.query.art_name.toString()

    return await handle(req, res, next, await where({ guild_id, art_id }));
  }
}

export function forCreateAttack(handle: Handler<Attack>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)
    
    return await handle(req, res, next, await create({ guild_id, data: req.body }));
  }
}

export function forEditAttack(handle: Handler<Attack>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)
    const id       = getAttackID(req)

    return await handle(req, res, next, await edit({ guild_id, id, data: req.body }))
  }
}

export function forDelAttack(handle: Handler<Attack>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)
    const id       = getAttackID(req)

    return await handle(req, res, next, await del({ guild_id, id }))
  }
}