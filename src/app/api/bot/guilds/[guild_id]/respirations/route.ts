import { respirations, forCreateRespiration } from 'middlewares/bot/art'
import { NextResponse } from 'next/server'

export const GET = respirations(async (req, { params }, { respirations }) => NextResponse.json(respirations))

export const POST = forCreateRespiration(async (req, { params }, { respiration }) => NextResponse.json(respiration))