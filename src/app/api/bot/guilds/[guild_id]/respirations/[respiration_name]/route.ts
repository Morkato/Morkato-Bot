import { respiration } from 'middlewares/bot/art'
import { NextResponse } from 'next/server'

export const GET = respiration(async (req, { params }, { respiration }) => NextResponse.json(respiration))