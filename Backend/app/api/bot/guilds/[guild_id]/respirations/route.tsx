import { NextRequest, NextResponse } from 'next/server'
import { authorization, respirations, guild_param } from 'middlewares/bot/database'

import { createRespiration } from 'models/arts'

export const GET = respirations(async (req, { params }, respirations) => NextResponse.json(respirations))

export const POST = guild_param(async (req, { params }, guild_id) => {
  const body = await req.json()

  const respiration = await createRespiration({ ...body, guild_id: guild_id })
  
  return NextResponse.json(respiration)
})