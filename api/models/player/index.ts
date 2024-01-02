import type { PlayerDatabase } from "type:models/player"
import type { Database } from "type:models/database"

import { wherePlayer } from './where'
import { getPlayer } from './get'
import { createPlayer } from './create'
import { editPlayer } from './edit'
import { deletePlayer } from './delete'

export function preparePlayerDatabase(database: Database): PlayerDatabase {
  const where  = wherePlayer(database)
  const get    = getPlayer(database)
  const create = createPlayer(database)
  const edit   = editPlayer(database)
  const del    = deletePlayer(database)

  return Object.freeze({ where, get, create, edit, del });
} // Function: preparePlayerDatabase

export default preparePlayerDatabase;