import { variable, forEditVar, forDelVar } from 'app/middlewares/bot/vars'
import { NextResponse } from 'next/server'

import { then, bot } from 'app/middlewares'

const GET = then(variable(async (req, ctx, { variable }) => NextResponse.json(variable)))
const POST = then(forEditVar(async (req, ctx, { after }) => NextResponse.json(after)))
const DELETE = then(forDelVar(async (req, { params }, { variable }) => NextResponse.json(variable)))