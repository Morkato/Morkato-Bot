import { kekkijutsus } from 'middlewares/bot/art'
import { NextResponse } from 'next/server'

export const GET = kekkijutsus(async (req, { params }, { kekkijutsus }) => NextResponse.json(kekkijutsus))