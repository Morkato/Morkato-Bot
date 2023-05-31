import type { NextResult, NextFunction, NextRequest, CustomContext } from 'middlewares'
import type { Guild } from 'models/validator/guild'

import { param } from 'middlewares/utils'
import { guild } from './guild'

import Arts, { Kekkijutsu, Respiration } from 'models/arts'

import client from 'infra/database'

const keys = {
  respiration_name: 'resp_name',
  kekkijutsu_name: 'kekki_name'
}

const arts = Arts(client.art)

export function respirations(handle: (req: NextRequest, ctx: CustomContext, props: { respirations: Respiration[], guild: Guild }) => NextResult): NextFunction {
  return guild(async (req, ctx, guild) => {
    const respirations = await arts.getArts({ guild, type: "RESPIRATION" })

    return await handle(req, ctx, { respirations, guild });
  })
}

export function respiration(handle: (req: NextRequest, ctx: CustomContext, props: { respiration: Respiration, guild: Guild }) => NextResult): NextFunction {
  return param(async (req, ctx, param) => {
    const middleware = guild(async (req, ctx, guild) => {
      const respiration = await arts.getArt({ guild, type: "RESPIRATION", name: param })

      return handle(req, ctx, { respiration, guild });
    })

    return middleware(req, ctx);
  }, keys['respiration_name'])
}

export function forCreateRespiration(handle: (req: NextRequest, ctx: CustomContext, props: { respiration: Respiration, guild: Guild }) => NextResult): NextFunction {
  return guild(async (req, ctx, guild) => {
    const respiration = await arts.createArt<"RESPIRATION">({ guild, art: await req.json() })

    return await handle(req, ctx, { respiration, guild });
  })
}

export function kekkijutsus(handle: (req: NextRequest, ctx: CustomContext, props: { kekkijutsus: Kekkijutsu[] }) => NextResult): NextFunction {
  return guild(async (req, ctx, guild) => {
    const kekkijutsus = await arts.getArts({ guild, type: "KEKKIJUTSU" })

    return await handle(req, ctx, { kekkijutsus });
  })
}

export function kekkijutsu(handle: (req: NextRequest, ctx: CustomContext, props: { kekkijutsu: Kekkijutsu, guild: Guild }) => NextResult): NextFunction {
  return param(async (req, ctx, param) => {
    const middleware = guild(async (req, ctx, guild) => {
      const kekkijutsu = await arts.getArt({ guild, type: "KEKKIJUTSU", name: param })

      return handle(req, ctx, { kekkijutsu, guild });
    })

    return middleware(req, ctx);
  }, keys['kekkijutsu_name'])
}
