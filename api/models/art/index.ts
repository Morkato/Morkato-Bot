import type { Database } from "type:models/database"
import type { ArtDatabase } from "type:models/art"

import { whereArt } from './where'
import { getArt } from './get'
import { createArt } from './create'
import { editArt } from './edit'
import { deleteArt } from './delete'

export function prepareDatabaseArt(database: Database): ArtDatabase {
  const where = whereArt(database)
  const get = getArt(database)
  const create = createArt(database)
  const edit = editArt(database)
  const del = deleteArt(database)

  return { where, get, create, edit, del };
} // Function: prepareDatabaseArt

export default prepareDatabaseArt;