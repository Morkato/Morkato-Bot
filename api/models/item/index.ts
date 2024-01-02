import type { ItemDatabase } from "type:models/item"
import type { Database } from "type:models/database"

import { whereItem } from './where'
import { getItem } from './get'
import { createItem } from './create'
import { editItem } from './edit'
import { deleteItem } from './delete'

export function prepareItemDatabase(database: Database): ItemDatabase {
  const where  = whereItem(database)
  const get    = getItem(database)
  const create = createItem(database)
  const edit   = editItem(database)
  const del    = deleteItem(database)

  return Object.freeze({ where, get, create, edit, del });
} // Function: prepareItemDatabase

export default prepareItemDatabase;