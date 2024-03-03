import type { ItemDatabase } from "type:models/item"
import type { Database } from "type:models/database"

import { whereItem } from './where'
import { getItem } from './get'
import { createItem } from './create'
import { editItem } from './edit'
import { deleteItem } from './delete'

export function prepareItemDatabase(database: Database): ItemDatabase {
  const find   = whereItem(database)
  const get    = getItem(database)
  const create = createItem(database)
  const edit   = editItem(database)
  const del    = deleteItem(database)

  return {
    findItem: find,
    getItem: get,
    createItem: create,
    editItem: edit,
    delItem: del
  };
} // Function: prepareItemDatabase

export default prepareItemDatabase;