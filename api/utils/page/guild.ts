import type { Request } from "express"

import { InternalServerError } from "errors"

export function extractGuildID(req: Request) {
  const id = req.params.guild_id
  
  if (typeof id === 'string') {
    return id;
  }

  throw new InternalServerError({
    message: "Erro interno",
    errorLocationCode: 'utils/page/guild'    
  })
}