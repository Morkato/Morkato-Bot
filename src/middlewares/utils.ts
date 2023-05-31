import type { CustomContext, NextResult } from "."

import { NextRequest, NextResponse } from "next/server"

import {
  BaseError,
  UnauthorizedError
} from 'errors'

export function param(handle: (req: NextRequest, ctx: CustomContext, param: string) => Promise<NextResponse>, param_key: string) {
  return async (req: NextRequest, { params }) => {
    const param = params[param_key]
    
    if(!param) {
      throw new UnauthorizedError({ message: `401: Parâmetro "${param_key}" é requerido.`, action: `Tente novamente com o parâmetro "${param}".` })
    }

    return handle(req, { params }, param);
  }
}

export async function defaultResponseError(error: Error | BaseError) {
  if(error instanceof BaseError) {
    return NextResponse.json({
      message: error.message,
      action: error.action,
      status: error.statusCode
    }, {
      status: error.statusCode
    })
  }

  return NextResponse.json({ error: error }, { status: 500 })
}

export function then<Params extends any[]>(handle: (...parmas: Params) => NextResult, catchError?: (err: Error | BaseError) => NextResult): (...parmas: Params) => NextResult {
  return async (...params: Params) => {
    try {
      return await handle(...params);
    } catch(err) {
      return catchError ? await catchError(err) : await defaultResponseError(err);
    }
  }
}
