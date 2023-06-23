import type { NextResult, NextFunction, NextRequest, CustomContext } from 'app/middlewares'

import Guilds, { type Guild } from 'models/guild'

import { param } from 'app/middlewares/utils'
import { authorization } from './utils'

import client from 'infra/database'

const guilds = Guilds(client.guild)

export function guild(handle: (req: NextRequest, ctx: CustomContext, guild: Guild) => NextResult): NextFunction {
  return authorization(param(async (req, ctx, id) => {
    return await handle(req, ctx, await guilds.get(id));
  }, 'guild_id'))
}