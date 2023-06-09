import { variables, forCreateVariable } from "middlewares/bot/vars";
import { NextResponse } from "next/server";

import { then, bot } from 'middlewares'

export const GET = then(variables(async (req, ctx, { variables }) => NextResponse.json(variables)))
export const POST = then(forCreateVariable(async (req, ctx, { variable }) => NextResponse.json(variable)))