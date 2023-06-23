/*
*  Rota: /api/bot/guilds/[guild_id]/art/[name]/attacks/[name]
*  
*  Possíveis errors:

*    UnauthorizedError
*    DatabaseError

*  :return [Guild: Object]:
*/

import { forCreateAttack } from "app/middlewares/bot/attack"
import { NextResponse } from "next/server"

export const POST = forCreateAttack(async (req, { params }, { attack }) => NextResponse.json(attack))