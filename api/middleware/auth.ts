import type { Request, Response, NextFunction } from 'express'
import type { User } from 'type:users'

import anonymous from  'anonymous'
import users     from 'users.json'

import 'type:middleware/auth'

export default () => {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = users.find(usr => usr.authorization === req.headers.authorization) ?? anonymous
  
    req.usr = user as User
  
    next();
  };
}