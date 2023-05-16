import { kekkijutsus, createKekki } from 'middlewares/bot'
import { NextResponse } from 'next/server'

export const GET = kekkijutsus(async (req, { params }, { kekkijutsus }) => NextResponse.json(kekkijutsus));

export const POST = createKekki(async (req, { params }, { kekkijutsu }) => NextResponse.json(kekkijutsu))