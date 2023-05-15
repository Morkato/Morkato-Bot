import type { CustomContext } from 'middlewares'

import { Guild, getGuild, createGuild, getGuilds } from 'models/guild'
import {
  Respiration,              Kekkijutsu,
  getRespiration,           getKekkijutsu,
  getRespirationsFromGuild, getKekkijutsusFromGuild
} from 'models/arts'
import { NextRequest, NextResponse } from 'next/server'

import {
  BaseError,
  UnauthorizedError,
  NotFoundError,
  InternalServerError
} from 'errors'

import * as middleware_discord from '..'
import { param } from 'middlewares/utils'

export const authorization = middleware_discord.authorization

export function guild(handle: (req: NextRequest, ctx: CustomContext, guild: Guild) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse> ) {
  return authorization(param(async (req, { params }, guild_id) => {
    let database_guild;
    try {
      console.log('aqui')
      database_guild = await getGuild(guild_id)
    } catch {
      console.log('aqui')
      database_guild = await createGuild({ id: guild_id })
      console.log('aqui')
    }

    return await handle(req, { params }, database_guild);
  }, 'guild_id'), catchError)
}

export function guilds(handle: (req: NextRequest, ctx: CustomContext, guilds: Guild[]) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return middleware_discord.guilds(async (req, ctx, guilds) => {
    const filteredGuilds = await getGuilds(guilds.map(guild => guild.id))
    
    return await handle(req, ctx, filteredGuilds);
  }, catchError)
}

export function respiration(handle: (req: NextRequest, ctx: CustomContext, respiration: Respiration) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return guild(async (req, { params }, guild) => {
    const database_respiration = await getRespiration(guild.id, params.respiration_name, { userName: 'Bot:Admin' })

    return await handle(req, { params }, database_respiration);
  }, catchError)
}

export function respirations(handle: (req: NextRequest, ctx: CustomContext, respirations: Respiration[]) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return guild(async (req, ctx, guild) => {
    const database_respirations = await getRespirationsFromGuild(guild.id, { userName: 'Bot:Admin' })

    return await handle(req, ctx, database_respirations)
  }, catchError)
}

export function kekkijutsu(handle: (req: NextRequest, ctx: CustomContext, kekkijutsu: Kekkijutsu) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return guild(async (req, { params }, guild) => {
    const database_kekkijutsu = await getKekkijutsu(guild.id, params.kekkijutsu_name, { userName: 'Bot:Admin' })

    return await handle(req, { params }, database_kekkijutsu);
  }, catchError)
}

export function kekkijutsus(handle: (req: NextRequest, ctx: CustomContext, kekkijutsus: Kekkijutsu[]) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return guild(async (req, { params }, guild) => {
    const database_kekkijutsus = await getKekkijutsusFromGuild(guild.id, { userName: 'Bot:Admin' })

    return await handle(req, { params }, database_kekkijutsus);
  }, catchError)
}