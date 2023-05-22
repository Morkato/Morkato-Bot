import { NextResponse } from 'next/server'
import { guild } from 'middlewares/bot'

export const GET = guild(async (req, { params }, { guild }) => NextResponse.json(guild))