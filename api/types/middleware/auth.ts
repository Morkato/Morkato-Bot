import type { User } from 'type:users'

declare global {
  export namespace Express {
    export interface Request {
      usr: User
    }
  }
}