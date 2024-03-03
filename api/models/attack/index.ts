import type { AttackDatabase } from "type:models/attack"
import type { Database } from "type:models/database"

import { whereAttack } from './where'
import { getAttack } from './get'
import { createAttack } from './create'
import { editAttack } from './edit'
import { deleteAttack } from './delete'

export function prepareAttackDatabase(database: Database): AttackDatabase {
  const find = whereAttack(database)
  const get = getAttack(database)
  const create = createAttack(database)
  const edit = editAttack(database)
  const del = deleteAttack(database)

  return {
    findAttack: find,
    getAttack: get,
    createAttack: create,
    editAttack: edit,
    delAttack: del
  };
} // Function: prepareDatabaseAttack

export default prepareAttackDatabase;