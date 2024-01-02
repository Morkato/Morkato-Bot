import type { PrismaClientKnownRequestError } from "@prisma/client/runtime/library"

import type { Attack, AttackNotifyType, AttackEditFunction, AttackEditParameter } from "type:models/attack"
import type { Database } from "type:models/database"

import { format, isUniqueAttackByName } from "utils/attack"
import { prismaError, errors } from "errors/prisma"
import { assert, schemas } from 'utils/schema'
import { uuid } from "utils/uuid"

import { ValidationError } from "errors"
import { validate } from 'schemas'

import { whereAttack } from './where'
import { getAttack } from './get'

function geterr(err: PrismaClientKnownRequestError, {
  guild_id,
  art_id,
  item_id,
  parent_id
}: Pick<Attack, 'guild_id'> & Partial<Pick<Attack, 'name' | 'art_id' | 'item_id' | 'parent_id'>>) {
  const type = prismaError(err)

  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  } else if (type === 'art.notfound') {
    return () => errors['art.notfound'](guild_id, art_id as string);
  } else if (type === 'item.notfound') {
    return () => errors['item.notfound'](guild_id, item_id as string);
  } else if (type === 'attack.notfound') {
    return () => errors['attack.notfound'](guild_id, parent_id as string);
  }

  return () => errors['generic.unknown']("Internal Error", "attack.create");
}

export function editAttack(database: Database): AttackEditFunction {
  const session = database.session.attack

  const where = whereAttack(database)
  const get   = getAttack(database)

  return async ({ guild_id, id, data }) => {
    guild_id = assert(schemas.id, guild_id)
    id       = assert(schemas.id,       id)
    
    const {
      name,
      required_exp,
      damage,
      breath,
      blood,
      exclude,
      embed_title,
      embed_description,
      embed_url
    } = validate(data, {
      name: 'optional',

      required_exp: 'optional',

      damage: 'optional',
      breath: 'optional',
      blood: 'optional',

      exclude: 'optional',

      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional'
    }) as AttackEditParameter['data']

    const before = await get({ guild_id, id })

    if (name && !isUniqueAttackByName({
      attacks: await where({ guild_id }),
      name: name,
      art_id: before.art_id,
      item_id: before.item_id,
      parent_id: before.parent_id
    })) {
      const error = errors['attack.alreadyexists']

      throw error(guild_id, name);
    }

    try {
      const prisma = await session.update({
        where: { guild_id_id: { guild_id, id } },
        data: {
          name: name,

          required_exp: required_exp,
          damage: damage,
          breath: breath,
          blood: blood,

          exclude: exclude === undefined ? undefined : exclude ? 'true' : 'false',

          embed_title: embed_title,
          embed_description: embed_description,
          embed_url: embed_url,

          updated_at: Date.now()
        }
      })

      const after = format(prisma)
      
      database.notify<AttackNotifyType, { before: Attack, after: Attack }>({ type: 'attack.edit', data: { before, after } })

      return after;
    } catch (err) {
      const error = geterr(err, { guild_id, art_id: before.art_id, item_id: before.item_id, parent_id: before.parent_id })

      throw error();
    }
  } // Function: Anonymous ({ guild_id, id, data })
} // Function: editAttack

export default editAttack;