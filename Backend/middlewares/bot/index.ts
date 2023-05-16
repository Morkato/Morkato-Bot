import { defaultResponseError, param, then } from 'middlewares/utils'
import { createGuild, getGuild, Guild } from 'models/guild'
import {
  Respiration,              Kekkijutsu,
  getRespirationsFromGuild, getKekkijutsusFromGuild,
  getRespiration,           getKekkijutsu,
  createRespiration,        createKekkijutsu,
  editRespiration,          editKekkijutsu
} from 'models/arts'
import { NextRequest, NextResponse } from 'next/server'
import { DynamicKeyValue } from 'utils'
import { CustomContext } from '..'

import {
  BaseError,
  UnauthorizedError
} from 'errors'

const settings = { userName: "Bot:Admin" }

export function authorization(handle: (req: NextRequest, ctx: CustomContext) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return then(async (req: NextRequest, ctx: CustomContext) => {
    if(process.env.BOT_TOKEN && req.headers.get('authorization') && req.headers.get('authorization') === process.env.BOT_TOKEN)
      return await handle(req, ctx);
    
    throw new UnauthorizedError({ message: '401: Unauthorized', action: 'Valide o token certo.' });
  }, catchError || defaultResponseError)
}

export function guild(handle: (req: NextRequest, ctx: CustomContext, { guild }: { guild: Guild }) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return authorization(param(async (req, ctx, id) => {
    let guild: Guild;
    
    try {
      guild = await getGuild(id, settings)
    } catch {
      guild = await createGuild({ id }, settings)
    }

    return await handle(req, ctx, { guild })
  }, 'guild_id'), catchError)
}

export function respirations(handle: (req: NextRequest, ctx: CustomContext, { guild, respirations }: { guild: Guild, respirations: Respiration[] }) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return guild(async (req, ctx, { guild }) => {
    return await handle(req, ctx, { guild, respirations:  await getRespirationsFromGuild(guild.id, settings)})
  }, catchError)
}

export function respiration(handle: (req: NextRequest, ctx: CustomContext, { guild, respiration }: { guild: Guild, respiration: Respiration }) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return guild(async (req, ctx, { guild }) => {
    return await param(async (req, ctx, name) => {
      return await handle(req, ctx, { guild, respiration: await getRespiration(guild.id, name, settings) })
    }, 'respiration_name')(req, ctx)
  }, catchError)
}

export function kekkijutsus(handle: (req: NextRequest, ctx: CustomContext, { guild, kekkijutsus }: { guild: Guild, kekkijutsus: Kekkijutsu[] }) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return guild(async (req, ctx, { guild }) => {
    return await handle(req, ctx, { guild, kekkijutsus: await getKekkijutsusFromGuild(guild.id, settings)})
  }, catchError)
}

export function kekkijutsu(handle: (req: NextRequest, ctx: CustomContext, { guild, kekkijutsu }: { guild: Guild, kekkijutsu: Kekkijutsu }) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return guild(async (req, ctx, { guild }) => {
    return await param(async (req, ctx, name) => {
      return await handle(req, ctx, { guild, kekkijutsu: await getKekkijutsu(guild.id, name, settings) })
    }, 'kekkijutsu_name')(req, ctx)
  }, catchError)
}

export function createResp(handle: (req: NextRequest, ctx: CustomContext, { guild, respiration }: { guild: Guild, respiration: Respiration }) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return guild(async (req, ctx, { guild }) => {
    return await handle(req, ctx, { guild, respiration: await createRespiration({ ...(await req.json()), guild_id: guild.id }) })
  }, catchError)
}

export function editResp(handle: (req: NextRequest, ctx: CustomContext, { guild, respiration }: { guild: Guild, respiration: Respiration }) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>)  {
  return respiration(async (req, ctx, { guild, respiration }) => {
    return await handle(req, ctx, { guild, respiration: await editRespiration(guild.id, respiration, await req.json()) })
  }, catchError)
}

export function createKekki(handle: (req: NextRequest, ctx: CustomContext, { guild, kekkijutsu }: { guild: Guild, kekkijutsu: Kekkijutsu }) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return guild(async (req, ctx, { guild }) => {
    return await handle(req, ctx, { guild, kekkijutsu: await createKekkijutsu({ ...(await req.json()), guild_id: guild.id }) })
  }, catchError)
}

export function editKekki(handle: (req: NextRequest, ctx: CustomContext, { guild, kekkijutsu }: { guild: Guild, kekkijutsu: Kekkijutsu }) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>)  {
  return respiration(async (req, ctx, { guild, respiration }) => {
    return await handle(req, ctx, { guild, kekkijutsu: await editKekkijutsu(guild.id, respiration, await req.json()) })
  }, catchError)
}