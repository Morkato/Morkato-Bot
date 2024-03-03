import type { Request, Response, NextFunction } from 'express'
import type { Logger } from 'type:logging'

export default (logger: Logger) => {
  return async (req: Request, res: Response, next: NextFunction) => {
    logger.debug("%s %s %s", req.method, req.usr.name, req.originalUrl)

    return next();
  };
}