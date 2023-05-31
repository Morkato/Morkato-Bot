import { NextResponse } from 'next/server'

import { then, bot } from 'middlewares'

const { guild } = bot.guild

/*
*  Rota: /api/bot/guilds/[guild_id]
*  
*  Possíveis errors:

*    UnauthorizedError
*    DatabaseError

*  :return [Guild: Object]:
*/

export const GET = then(guild(async (req, { params }, guild) => NextResponse.json(guild)))