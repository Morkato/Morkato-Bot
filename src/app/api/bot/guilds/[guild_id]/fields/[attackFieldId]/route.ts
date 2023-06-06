import { attackField, forEditAttackField, forDelAttackField } from "base:middlewares/bot/attack_field"
import { NextResponse } from 'next/server'

export const GET = attackField(async (req, { params }, { field }) => NextResponse.json(field))
export const POST = forEditAttackField(async (req, { params }, { afterField }) => NextResponse.json(afterField))
export const DELETE = forDelAttackField(async (req, { params }, { field }) => NextResponse.json(field))