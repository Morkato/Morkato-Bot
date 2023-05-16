import { respiration, editResp } from 'middlewares/bot'
import { NextResponse } from 'next/server'

export const GET = respiration(async (req, { params }, { respiration }) => NextResponse.json(respiration));

export const POST = editResp(async (req, { params }, { respiration }) => NextResponse.json(respiration))
