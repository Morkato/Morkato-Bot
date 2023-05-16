import { kekkijutsu, editKekki } from 'middlewares/bot'
import { NextResponse } from 'next/server'

export const GET = kekkijutsu(async (req, { params }, { kekkijutsu }) => NextResponse.json(kekkijutsu))

export const POST = editKekki(async (req, { params }, { kekkijutsu }) => NextResponse.json(kekkijutsu))