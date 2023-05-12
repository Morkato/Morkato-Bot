import type { CustomContext } from 'middlewares'

import { Guild, getGuild, createGuild, getGuilds } from 'models/guild'
import {
  Respiration,              Kekkijutsu,
  getRespiration,           getKekkijutsu,
  getRespirationsFromGuild, getKekkijutsusFromGuild
} from 'models/arts'
import { NextRequest, NextResponse } from 'next/server'

import { BaseError } from 'erros'

import * as middleware_discord from '..'

export function guild(handle: (req: NextRequest, ctx: CustomContext, guild: Guild) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse> ) {
  return middleware_discord.guild(async (req, ctx, guild) => {
    let database_guild;
    try {
      database_guild = await getGuild(guild.id)
    } catch {
      database_guild = await createGuild({ id: guild.id })
    }

    return await handle(req, ctx, database_guild);
  }, catchError)
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
  })
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