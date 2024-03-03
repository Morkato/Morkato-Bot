import type { Handler, Request } from 'express'

import { InternalServerError } from 'errors'

import error from 'error'

export function then(handler: Handler): Handler {
  return async (req, res, next) => {
    try {
      const result = handler(req, res, next)

      if ((result as any) instanceof Promise) {
        await result
      }
    } catch (err) {
      error(err, req, res)
    }
  }
}

export function extractParam(req: Request, name: string): string {
  const id = req.params[name]
  
  if (typeof id === 'string') {
    return id;
  }

  throw new InternalServerError({
    message: "Erro interno",
    errorLocationCode: 'utils/page/guild'    
  })
}