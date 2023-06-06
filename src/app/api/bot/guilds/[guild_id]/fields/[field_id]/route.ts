import { attackField, forEditAttackField, forDelAttackField } from "middlewares/bot/attack_field"
import { NextResponse } from 'next/server'

import { then } from 'middlewares'

export const GET = then(attackField(async (req, { params }, { field }) => NextResponse.json(field)))
export const POST = then(forEditAttackField(async (req, { params }, { afterField }) => NextResponse.json(afterField)))
export const DELETE = then(forDelAttackField(async (req, { params }, { field }) => NextResponse.json(field)))