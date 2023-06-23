import type { NextRequest, NextResponse } from 'next/server'

export * as bot from './bot/index'
export * from './utils'

export type CustomContext = { params: Record<string, string> }
export type NextResult = NextResponse | Promise<NextResponse>;
export type NextFunction<T extends unknown = unknown> = (req: NextRequest, ctx: T) => NextResult;

export type { NextRequest };