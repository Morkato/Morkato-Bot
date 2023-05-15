import type { CustomContext } from "."

import { NextRequest, NextResponse } from "next/server"

import {
  BaseError,
  UnauthorizedError
} from 'errors'

export function param(handle: (req: NextRequest, ctx: CustomContext, param: string) => Promise<NextResponse>, param_key: string) {
  return async (req: NextRequest, { params }) => {
    const param = params[param_key]
    
    if(!param)
      throw new UnauthorizedError({ message: `401: Parâmerto "${param_key}" é requerido.`, action: 'Tente novamente com o parâmerto "guild_id".' })

    return handle(req, { params }, param);
  }
}

export async function defaultResponseError(error: Error | BaseError) {
  if(error instanceof BaseError)
    return NextResponse.json({
      message: error.message,
      action: error.action,
      status: error.statusCode
    }, {
      status: error.statusCode
    })

  return NextResponse.json({ error: error }, { status: 500 })
}

export function then<Params extends any[], Return>(handle: (...parmas: Params) => Return, catchError: (err: Error | BaseError) => Return): (...parmas: Params) => Promise<Return> {
  return async (...params: Params) => {
    try {
      return await handle(...params);
    } catch(err) {
      console.error(err)

      return await catchError(err);
    }
  }
}
