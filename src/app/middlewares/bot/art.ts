import type { NextResult, NextRequest, CustomContext, NextFunction } from 'app/middlewares'
import type { Guild } from 'models/validator/guild'

import { param } from 'app/middlewares/utils'
import { guild } from './guild'

import Arts, { type Art } from 'models/arts'

import client from 'infra/database'

const arts = Arts(client.art)

export function allArts(handle: (req: NextRequest, ctx: CustomContext, { guild, arts }: { guild: Guild, arts: Art[]}) => NextResult) {
  /**
   * :async middleware:
   * 
   * Context Returning { guild, arts }
   * 
   * Parâmetros aceitados:
   *  - map : 'RESPIRATION' | 'KEKKIJUTSU'
   *
   *    Exemplos:
   *      .../?map=RESPIRATION -> Irá filtrar apenas as respirações.
   * 
   * @returns { NextFunction }
   */

  return guild(async (req, ctx, guild) => {
    const type = req.nextUrl.searchParams.get('map')

    const allArts = await arts.getAll(guild)

    return await handle(req, ctx, { guild, arts: !type ? allArts : allArts.filter(art => art.type === type)})
  })
}

export function art(handle: (req: NextRequest, ctx: CustomContext, { guild, art }: { guild: Guild, art: Art }) => NextResult) {
  return param(async (req, ctx, name) => {
    return await guild(async (req, ctx, guild) => {
      const art = await arts.get({ guild, name })

      return await handle(req, ctx, { guild, art })
    })(req, ctx)
  }, 'art_name')
}

export function forCreateArt(handle: (req: NextRequest, ctx: CustomContext, { guild, art }: { guild: Guild, art: Art }) => NextResult) {
  return guild(async (req, ctx, guild) => {
    const art = await arts.create({ guild, data: await req.json() })

    return await handle(req, ctx, { guild, art })
  })
}

export function forEditArt(handle: (req: NextRequest, ctx: CustomContext, { guild, beforeArt, afterArt }: { guild: Guild, beforeArt: Art, afterArt: Art }) => NextResult) {
  return art(async (req, ctx, { guild, art }) => {
    const afterArt = await arts.editArt({ guild, art, data: await req.json() })

    return await handle(req, ctx, { guild, beforeArt: art, afterArt });
  })
}

export function forDelArt(handle: (req: NextRequest, ctx: CustomContext, { guild, art }: { guild: Guild, art: Art }) => NextResult) {
  return art(async (req, ctx, { guild, art }) => {
    const deletedArt = await arts.delArt({ guild, art })

    return await handle(req, ctx, { guild, art: deletedArt });
  })
}