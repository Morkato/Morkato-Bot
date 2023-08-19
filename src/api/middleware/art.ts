import type { Handler as ExpressHandler, Request } from 'express'
import type { Art }   from 'models/arts'
import type { Handler } from '.'

import { getGuildID } from './guild'

import { InternalServerError } from 'errors'

import Arts from 'models/arts'

import client from 'infra/database'

const {
  where,
  create,
  edit,
  del,
  get
} = Arts(client.art)

export function getArtID(req: Request) {
  if (!req.params.name) {
    throw new InternalServerError({ message: "Erro interno no servidor" })
  }

  return req.params.name;
}

export function getArtType(req: Request) {
  if (!req.query.art_type) {
    return;
  }

  const type = req.query.art_type.toString().toLocaleLowerCase()

  return (
    [ 'r', 'resp', 'respiration' ].includes(type)
    ? 'RESPIRATION'
    : (
      [ 'k', 'kekki', 'kekkijutsu' ].includes(type)
      ? 'KEKKIJUTSU'
      : undefined
    )
  );
}

export function art(handle: Handler<Art>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)
    const id       = getArtID(req)

    return await handle(req, res, next, await get({ guild_id, id }));
  }
}

export function arts(handle: Handler<Art[]>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)
    const type     = getArtType(req)

    return await handle(req, res, next, await where({ guild_id, type }));
  }
}

export function forCreateArt(handle: Handler<Art>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)

    return await handle(req, res, next, await create({ guild_id, data: req.body }));
  }
}

export function forEditArt(handle: Handler<{ before: Art, after: Art }>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)
    const id       = getArtID(req)

    const before = await get({ guild_id, id })
    const after  = await edit({ guild_id, id, data: req.body })

    return await handle(req, res, next, { before, after });
  }
}

export function forDelArt(handle: Handler<Art>): ExpressHandler {
  return async (req, res, next) => {
    const guild_id = getGuildID(req)
    const id       = getArtID(req)

    return await handle(req, res, next, await del({ guild_id, id }))
  }
}