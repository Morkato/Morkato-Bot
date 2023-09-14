import type { Handler as ExpressHandler, Request } from 'express'
import type { Guild }   from 'models/guild'
import type { Handler } from '.'

import { InternalServerError } from 'errors'

import Guilds from 'models/guild'

import client from 'infra/database'

const guilds = Guilds(client.guild)

export function getGuildID(req: Request) {
  const value = req.params['guild_id']  

  if (!value) {
    throw new InternalServerError({ message: "Erro interno no servidor <getGuildID>" })
  }

  return value;
}

export default function guild(handle: Handler<Guild>): ExpressHandler {
  return async (req, res, next) => {
    const id = getGuildID(req)

    await handle(req, res, next, await guilds.get(id))
  }
}

export { guild };