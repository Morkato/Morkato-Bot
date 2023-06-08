import { PrismaClient, Prisma } from '@prisma/client'

export const prisma = new PrismaClient({
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



export default prisma;