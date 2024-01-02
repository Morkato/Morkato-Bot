import type { AttackDatabase } from "type:models/attack"
import type { Database } from "type:models/database"

import { whereAttack } from './where'
import { getAttack } from './get'
import { createAttack } from './create'
import { editAttack } from './edit'
import { deleteAttack } from './delete'

export function prepareDatabaseAttack(database: Database): AttackDatabase {
  const where = whereAttack(database)
  const get = getAttack(database)
  const create = createAttack(database)
  const edit = editAttack(database)
  const del = deleteAttack(database)

  return { where, get, create, edit, del };
} // Function: prepareDatabaseAttack

export default prepareDatabaseAttack;