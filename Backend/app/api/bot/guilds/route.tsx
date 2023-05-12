import { guilds } from 'middlewares/bot/database'
import { NextResponse } from 'next/server'

export const GET = guilds(async (req, { params }, guilds) => {
  return NextResponse.json(guilds);
})