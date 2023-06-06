import { attacksFields, forCreateAttackField } from "middlewares/bot/attack_field"
import { NextResponse } from 'next/server'

import { then } from "middlewares"

export const GET = then(attacksFields(async (req, { params }, { fields }) => NextResponse.json(fields)))
export const POST = then(forCreateAttackField(async (req, { params }, { field }) => NextResponse.json(field)))