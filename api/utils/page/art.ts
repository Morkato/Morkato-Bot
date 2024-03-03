import type { Request } from "express"

import { extractParam } from "./etc"

export function extractArtID(req: Request) {
  return extractParam(req, 'art_id')
}