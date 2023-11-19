export { object } from './object'
export { string } from './string'

import { BaseError, InternalServerError } from 'morkato/errors'

import type { Handler, Request, Response, NextFunction } from "express"

type SendType = 'json' | 'text'

const sendEvents = {
  json: (res: Response, obj: any) => res.json(obj),
  text: (res: Response, obj: any) => res.send(obj)
}

export function then<Params extends any[]>(handle: Handler): Handler {
  return async (req, res, next) => {
    try {
      return await handle(req, res, next);
    } catch (err) {
      if (err instanceof BaseError) {
        console.error(err)

        res.status(err.statusCode || 500).json({ message: err.message, action: err.action })

        return
      }

      res.status(500).json({ message: 'InternalErrorServer', error: err })
    }
  }
}

export function sender<T extends any = {}>(type: SendType) {
  const event = sendEvents[type]

  if (!event) {
    throw new Error('Type Send not exists!')
  }

  return async (req: Request, res: Response, next: NextFunction, obj: T) => {
    event(res, obj)
  }
}