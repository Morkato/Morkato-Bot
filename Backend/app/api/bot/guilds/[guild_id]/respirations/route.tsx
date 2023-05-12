import { NextRequest, NextResponse } from 'next/server'
import { guild, respirations } from 'middlewares/bot/database'

import { createRespiration } from 'models/arts'

export const GET = respirations(async (req, { params }, respirations) => NextResponse.json(respirations))

export const POST = guild(async (req, { params }, guild) => {
  const body = await req.json()

  const respiration = await createRespiration({ ...body, guild_id: guild.id })
  
  return NextResponse.json(respiration)
})