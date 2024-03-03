import type { PlayerArtDatabase } from "type:models/playerArt"
import type { Database } from "type:models/database"

import wherePlayerArt from './where'
import getPlayerArt from './get'

export function prepareDatabasePlayerArt(database: Database): PlayerArtDatabase {
  return {
    findPlayerArt: wherePlayerArt(database),
    getPlayerArt: getPlayerArt(database)
  } as PlayerArtDatabase
}

export default prepareDatabasePlayerArt;