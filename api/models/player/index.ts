import type { PlayerDatabase } from "type:models/player"
import type { Database } from "type:models/database"

import { wherePlayer } from './where'
import { getPlayer } from './get'
import { createPlayer } from './create'
import { editPlayer } from './edit'
import { deletePlayer } from './delete'

export function preparePlayerDatabase(database: Database): PlayerDatabase {
  return {
    findPlayer: wherePlayer(database),
    getPlayer: getPlayer(database),
    createPlayer: createPlayer(database),
    editPlayer: editPlayer(database),
    delPlayer: deletePlayer(database)
  };
} // Function: preparePlayerDatabase

export default preparePlayerDatabase;