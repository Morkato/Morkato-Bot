import { attacksFields, forCreateAttackField } from "middlewares/bot/attack_field"
import { NextResponse } from 'next/server'

export const GET = attacksFields(async (req, { params }, { fields }) => NextResponse.json(fields))
export const POST = forCreateAttackField(async (req, { params }, { field }) => NextResponse.json(field))