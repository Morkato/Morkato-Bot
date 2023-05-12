import { kekkijutsu } from 'middlewares/bot/database'
import { editKekkijutsu } from 'models/arts'
import { NextResponse } from 'next/server'

export const GET = kekkijutsu(async (req, ctx, kekkijutsu) => NextResponse.json(kekkijutsu))

export const POST = kekkijutsu(async (req, ctx, kekkijutsu) => {
  const editedKekkijutsu = await editKekkijutsu(kekkijutsu, await req.json())

  return NextResponse.json(editedKekkijutsu)
})