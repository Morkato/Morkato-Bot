import type { NextFunction } from 'app/middlewares'

import {
  UnauthorizedError
} from 'errors'

export function authorization(handle: NextFunction): NextFunction {
  return async (req, ctx) => {
    if(req.headers.get('authorization') === process.env.BOT_TOKEN) {
      return await handle(req, ctx);
    }

    throw new UnauthorizedError({
      message: "Você não é autorizado para fazer esse serviço."
    })
  }
}