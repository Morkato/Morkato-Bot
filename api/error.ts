import type { Request, Response } from "express"

import { BaseError } from "errors"

export default (err: any, req: Request, res: Response) => {
  if (err instanceof BaseError) {
    res.status(err.statusCode ?? 500).json({
      message: err.message,
      action: err.action,
      extends: err.type,
      location: err.errorLocationCode
    })
    
    return;
  }

  console.error(err)

  res.status(500).json({
    message: "Erro interno",
    action: "Notifique a um desenvolvedor.",
    extends: 'generic.unknown',
  })
}