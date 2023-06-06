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

import { then } from "middlewares"

export const GET = then(attack(async (req, { params }, { attack }) => NextResponse.json(attack)))
export const POST = then(forEditAttack(async (req, { params }, { attack }) => NextResponse.json(attack)))
export const DELETE = then(forDelAttack(async (req, { params }, { attack }) => NextResponse.json(attack)))