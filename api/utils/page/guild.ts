import type { Request } from "express"

import { extractParam } from "./etc"

export function extractGuildID(req: Request) {
  return extractParam(req, 'guild_id')
}