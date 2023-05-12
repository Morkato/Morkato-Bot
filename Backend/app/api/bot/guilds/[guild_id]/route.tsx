import { guild } from 'middlewares/bot/database'
import { NextResponse } from "next/server"

export const GET = guild(async (req, ctx, guild) => NextResponse.json(guild))