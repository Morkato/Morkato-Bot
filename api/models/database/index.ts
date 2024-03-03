import type { Database, Subscriber } from 'type:models/database'

import { PrismaClient } from '@prisma/client'

import preparePlayerItemDatabase from 'models/playerItem'
import preparePlayerArtDatabase from 'models/playerArt'
import preparePlayerDatabase from 'models/player'
import prepareAttackDatabase from 'models/attack'
import prepareGuildDatabase from 'models/guild'
import prepareItemDatabase from 'models/item'
import prepareArtDatabase from 'models/art'

import { subscribe } from './subscribe'
import { notify } from './notify'

export function prepareDatabase(): Database {
  const session = new PrismaClient()
  const observers: Subscriber[] = []
  
  const database: Database = {
    session: session,
    observers: observers,
    subscribe: subscribe(observers),
    notify: notify(observers)
  } as Database

  Object.assign(
    database,
    
    preparePlayerItemDatabase(database),
    preparePlayerArtDatabase(database),
    preparePlayerDatabase(database),
    prepareAttackDatabase(database),
    prepareGuildDatabase(database),
    prepareItemDatabase(database),
    prepareArtDatabase(database)
  )
  
  return Object.freeze(database);
}

export default prepareDatabase;