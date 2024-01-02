import type { PlayerItemDatabase } from 'type:models/playerItem'
import type { Database } from 'type:models/database'

import { wherePlayerItem } from './where'
import { getPlayerItem } from './get';
import { createPlayerItem } from './create'
import { editPlayerItem } from './edit'
import { deletePlayerItem } from './delete'

export function prepareDatabasePlayerItem(database: Database): PlayerItemDatabase {
  const where  = wherePlayerItem(database)
  const get    = getPlayerItem(database)
  const create = createPlayerItem(database)
  const edit   = editPlayerItem(database)
  const del    = deletePlayerItem(database)

  return Object.freeze({ where, get, create, edit, del });
}

export default prepareDatabasePlayerItem;