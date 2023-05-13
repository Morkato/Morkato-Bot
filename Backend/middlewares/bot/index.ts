import type {
  Guild,
  User
} from 'utils/discordApi'

import { NextRequest, NextResponse } from 'next/server'
import { defaultResponseError, param, then } from 'middlewares/utils'
import { DynamicKeyValue } from 'utils'
import { CustomContext } from '..'

import {
  BaseError,
  UnauthorizedError,
  NotFoundError,
  InternalServerError
} from 'erros'

import discord from 'utils/discordApi'

export function authorization(handle: (req: NextRequest, ctx: { params: DynamicKeyValue<string> }) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return then(async (req: NextRequest, ctx: { params: DynamicKeyValue<string> }) => {
    if(process.env.BOT_TOKEN && req.headers.get('authorization') && req.headers.get('authorization') === process.env.BOT_TOKEN)
      return await handle(req, ctx);
    
    throw new UnauthorizedError({ message: '401: Unauthorized', action: 'Valide o token certo.' });
  }, catchError || defaultResponseError)
}

export function guild(handle: (req: NextRequest, ctx: { params: DynamicKeyValue<string> }, guild: Guild) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return authorization(param(async (req, { params }: { params: DynamicKeyValue<string> }, guild_id) => {
    const api = discord(`Bot ${process.env.BOT_TOKEN}`)

    const guild = await api.guild(guild_id)
    
    return await handle(req, { params }, guild);
  }, 'guild_id'), catchError)
}

export function guilds(handle: (req: NextRequest, ctx: CustomContext, guilds: Guild[]) => Promise<NextResponse>, catchError?: (err: Error | BaseError) => Promise<NextResponse>) {
  return authorization(async (req, ctx) => {
    const api = discord(`Bot ${process.env.BOT_TOKEN}`)

    const guilds = await api.guilds()

    return await handle(req, ctx, guilds);
  }, catchError)
}