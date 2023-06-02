/**
 * /apt/bot/guilds/[id]/arts/[name]
 * 
 *   AllowedMethods: 
 *     
 *     >> GET
 *     >> POST
 */

import { art } from 'middlewares/bot/art'
import { then } from 'middlewares/utils'
import { NextResponse } from 'next/server'

export const GET = then(art(async (req, { params }, { art }) => NextResponse.json(art)))