/*
*  Rota: /api/bot/guilds/[guild_id]/attacks/[name]
*  
*  Possíveis errors:

*    UnauthorizedError
*    DatabaseError

*  :return [Guild: Object]:
*/

import { attack, forEditAttack, forDelAttack } from "middlewares/bot/attack"
import { NextResponse } from "next/server"

export const GET = attack(async (req, { params }, { attack }) => NextResponse.json(attack))
export const POST = forEditAttack(async (req, { params }, { attack }) => NextResponse.json(attack))
export const DELETE = forDelAttack(async (req, { params }, { attack }) => NextResponse.json(attack))