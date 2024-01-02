import type { Request } from "express"

import { InternalServerError } from "errors"

export function extractArtID(req: Request) {
  const id = req.params.art_id

  if (typeof id === 'string') {
    return id;
  }

  throw new InternalServerError({
    message: "Erro interno",
    errorLocationCode: 'utils/page/art'    
  })
}