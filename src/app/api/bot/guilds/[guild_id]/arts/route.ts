/**
 * /apt/bot/guilds/[id]/arts
 * 
 *   AllowedMethods: 
 *     
 *     >> GET
 *     >> POST
 */

import { getArts } from 'middlewares/bot/art'
import { then } from 'middlewares/utils'
import { NextResponse } from 'next/server'

export const GET = then(getArts(async (req, { params }, { arts }) => NextResponse.json(arts)))