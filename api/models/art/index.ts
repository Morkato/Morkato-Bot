import type { ArtDatabase } from "type:models/art"
import type { Database } from "type:models/database"

import { whereArt } from './where'
import { getArt } from './get'
import { createArt } from './create'
import { editArt } from './edit'
import { deleteArt } from './delete'

export function prepareArtDatabase(database: Database): ArtDatabase {
  const find = whereArt(database)
  const get = getArt(database)
  const create = createArt(database)
  const edit = editArt(database)
  const del = deleteArt(database)

  return {
    findArt: find,
    getArt: get,
    createArt: create,
    editArt: edit,
    delArt: del
  };
} // Function: prepareArtDatabase

export default prepareArtDatabase;