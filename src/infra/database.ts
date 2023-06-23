import { PrismaClient, Prisma } from 'client'

declare global {
  let client: PrismaClient | undefined;
}

export const prisma = globalThis.client ?? new PrismaClient({
  log: ['query', 'info', 'warn', 'error']
})

function middleware(model: Prisma.MiddlewareParams['model'], action: Prisma.MiddlewareParams['action'] | Prisma.MiddlewareParams['action'][], func: Prisma.Middleware): Prisma.Middleware  {
  return async (params, next) => {
    if(params.model === model && (Array.isArray(action)) ? action.includes(params.action) : params.action === action) {
      return await func(params, next);
    }

    return await next(params)
  }
}

if (!globalThis.client) {
  globalThis.client = prisma
}

export default prisma;
