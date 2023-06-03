/**
 * /apt/bot/guilds/[id]/arts/[name]
 * 
 *   AllowedMethods: 
 *     
 *     >> GET
 *     >> POST
 *     >> DELETE
 */

import { art, forEditArt, forDelArt } from 'middlewares/bot/art'
import { then } from 'middlewares/utils'
import { NextResponse } from 'next/server'

export const GET = then(art(async (req, { params }, { art }) => NextResponse.json(art)))
export const POST = then(forEditArt(async (req, { params }, { afterArt }) => NextResponse.json(afterArt)))
export const DELETE = then(forDelArt(async (req, { params }, { art }) => NextResponse.json(art)))