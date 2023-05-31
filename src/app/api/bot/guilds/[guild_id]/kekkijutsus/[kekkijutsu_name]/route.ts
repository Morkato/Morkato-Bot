import { kekkijutsu } from 'middlewares/bot/art'
import { NextResponse } from 'next/server'

export const GET = kekkijutsu(async (req, { params }, { kekkijutsu }) => NextResponse.json(kekkijutsu))