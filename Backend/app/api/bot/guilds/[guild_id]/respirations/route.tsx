import { respirations, createResp } from 'middlewares/bot'
import { NextResponse } from 'next/server'

export const GET = respirations(async (req, { params }, { respirations }) => NextResponse.json(respirations));

export const POST = createResp(async (req, { params }, { respiration }) => NextResponse.json(respiration));