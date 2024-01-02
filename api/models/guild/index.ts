import type { GuildDatabase } from "type:models/guild"
import type { Database } from "type:models/database"

import { whereGuild } from './where'
import { getGuild } from './get'
import { createGuild } from './create'
import { deleteGuild } from './delete'

export function prepareDatabaseGuild(database: Database): GuildDatabase {
  const where = whereGuild(database)
  const get   = getGuild(database)
  const create = createGuild(database)
  const del = deleteGuild(database)

  return Object.freeze({ where, get, create, del });
} // Function: prepareDatabaseGuild

export default prepareDatabaseGuild;