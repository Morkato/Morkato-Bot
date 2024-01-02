import type { Handler, Request } from 'express'

import { BaseError, InternalServerError } from 'errors'

export function then(handler: Handler): Handler {
  return async (req, res, next) => {
    try {
      const result = handler(req, res, next) as any

      if (result instanceof Promise) {
        await result
      }
    } catch (err) {
      console.error(err)

      if (err instanceof BaseError) {
        res.status(err.statusCode ?? 500).json({
          message: err.message,
          action: err.action,
          extends: err.type,
          route: handler.name === "" ? "anonymous" : handler.name,
          location: err.errorLocationCode
        })
        
        return;
      }

      res.status(500).json({
        message: "Erro interno",
        action: "Notifique a um desenvolvedor.",
        extends: 'generic.unknown',
        handler: handler.name
      })
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