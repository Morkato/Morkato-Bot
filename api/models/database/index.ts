import type { Database, Subscriber } from 'type:models/database'

import { PrismaClient } from '@prisma/client'

import { subscribe } from './subscribe'
import { notify } from './notify'

export function prepareDatabase(): Database {
  const session = new PrismaClient()
  const observers: Subscriber[] = []
  
  const database: Database = {
    session: session,
    subscribe: subscribe(observers),
    notify: notify(observers)
  }

  /** All models */
  
  return database;
}

export default prepareDatabase;