import type { NextResult, NextFunction, NextRequest, CustomContext } from 'middlewares'
import type { Guild } from 'models/validator/guild'

import { param } from 'middlewares/utils'
import { guild } from './guild'

import Arts, { ArtType, Art, Respiration, Kekkijutsu } from 'models/arts'

import client from 'infra/database'

const arts = Arts(client.art)

export function getArts(handle: (req: NextRequest, ctx: CustomContext, { guild, arts }: { guild: Guild, arts: 
  (typeof ctx)['params']['map'] extends 'RESPIRATION'
  ? Respiration[]
  : (typeof ctx)['params']['map'] extends 'KEKKIJUTSU'
  ? Kekkijutsu[]
  : Art<ArtType>[]
}) => NextResult) {
  return guild(async (req, ctx, guild) => {
    const type = req.nextUrl.searchParams.get('map')

    const allArts = await arts.getArts(guild)

    return await handle(req, ctx, { guild, arts: !type ? allArts : allArts.filter(art => art.type === type)})
  })
}

export function art(handle: (req: NextRequest, ctx: CustomContext, { guild, art }: { guild: Guild, art: Art<ArtType> }) => NextResult) {
  return param(async (req, ctx, name) => {
    return await guild(async (req, ctx, guild) => {
      const art = await arts.getArt({ guild, name })

      return await handle(req, ctx, { guild, art })
    })(req, ctx)
  }, 'art_name')
}

export function forCreateArt(handle: (req: NextRequest, ctx: CustomContext, { guild, art }: { guild: Guild, art: Art<ArtType> }) => NextResult) {
  return guild(async (req, ctx, guild) => {
    const art = await arts.createArt({ guild, data: await req.json() })

    return await handle(req, ctx, { guild, art })
  })
}

export function forEditArt(handle: (req: NextRequest, ctx: CustomContext, { guild, beforeArt, afterArt }: { guild: Guild, beforeArt: Art<ArtType>, afterArt: Art<ArtType> }) => NextResult) {
  return art(async (req, ctx, { guild, art }) => {
    const afterArt = await arts.editArt({ guild, art, data: await req.json() })

    return await handle(req, ctx, { guild, beforeArt: art, afterArt });
  })
}

export function forDelArt(handle: (req: NextRequest, ctx: CustomContext, { guild, art }: { guild: Guild, art: Art<ArtType> }) => NextResult) {
  return art(async (req, ctx, { guild, art }) => {
    const deletedArt = arts.delArt({ guild, art })

    return await handle(req, ctx, { guild, art });
  })
}