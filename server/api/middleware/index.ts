import type { Request, Response, NextFunction } from 'express'

export type Handler<T = undefined> = (req: Request, res: Response, next: NextFunction, obj: T) => Promise<void>