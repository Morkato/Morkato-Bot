import { attackField, forEditAttackField } from "base:middlewares/bot/attack_field"
import { NextResponse } from 'next/server'

export const GET = attackField(async (req, { params }, { field }) => NextResponse.json(field))
export const POST = forEditAttackField(async (req, { params }, { afterField }) => NextResponse.json(afterField))