import type { NextResult, NextFunction, NextRequest, CustomContext } from 'middlewares'

import Guilds, { Guild } from 'models/guild'

import { param } from 'middlewares/utils'
import { authorization } from './utils'

import client from 'infra/database'


const guilds = Guilds(client.guild)

export function guild(handle: (req: NextRequest, ctx: CustomContext, guild: Guild) => NextResult): NextFunction {
  return authorization(param(async (req, ctx, param) => {
    let guild: Guild;

    try {
      guild = await guilds.getGuild(param)
    } catch {
      guild = await guilds.createGuild({ id: param })
    }

    return await handle(req, ctx, guild);
  }, 'guild_id'))
}