import type { GuildDatabase } from "type:models/guild"
import type { Database } from "type:models/database"

import { whereGuild } from './where'
import { getGuild } from './get'
import { createGuild } from './create'
import { deleteGuild } from './delete'

export function prepareDatabaseGuild(database: Database): GuildDatabase {
  return {
    findGuild: whereGuild(database),
    getGuild: getGuild(database),
    createGuild: createGuild(database),
    delGuild: deleteGuild(database)
  };
} // Function: prepareDatabaseGuild

export default prepareDatabaseGuild;