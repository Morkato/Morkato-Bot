import { guild, kekkijutsu } from 'middlewares/bot/database'
import { createKekkijutsu } from 'models/arts'
import { NextResponse } from 'next/server'

export const GET = kekkijutsu(async (req, { params }, kekkijutsus) => NextResponse.json(kekkijutsus))

export const POST = guild(async (req, { params }, guild) => {
  const body = await req.json()

  const kekkijutsu = await createKekkijutsu({ ...body, guild_id: guild.id })

  return NextResponse.json(kekkijutsu)
})