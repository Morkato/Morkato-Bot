import type { Handler } from "express"

import { BaseError } from 'errors'

export function then<Params extends any[]>(handle: Handler): Handler {
  return async (req, res, next) => {
    try {
      return await handle(req, res, next);
    } catch(err) {
      if (err instanceof BaseError) {
        console.error(err)
        
        res.status(err.statusCode || 500).json({ message: err.message, action: err.action })

        return
      }

      res.status(500).json({ message: 'InternalErrorServer', error: err })
    }
  }
}