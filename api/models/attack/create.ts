import type { PrismaClientKnownRequestError } from "@prisma/client/runtime/library"

import type { Attack, AttackNotifyType, AttackCreateFunction, AttackCreateParameter } from "type:models/attack"
import type { Database } from "type:models/database"

import { format, isUniqueAttackByName } from "utils/attack"
import { prismaError, errors } from "errors/prisma"
import { assert, schemas } from 'utils/schema'
import { uuid } from "utils/uuid"

import { ValidationError } from "errors"
import { validate } from 'schemas'

import { whereAttack } from './where'

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

export function createAttack(database: Database): AttackCreateFunction {
  const session = database.session.attack

  const where = whereAttack(database)

  return async ({ guild_id, data }) => {
    guild_id = assert(schemas.id, guild_id)

    const {
      name,
      required_exp,
      damage,
      breath,
      blood,
      exclude,
      embed_title,
      embed_description,
      embed_url,
      item_id,
      art_id,
      parent_id
    } = validate(data, {
      name: 'required',

      required_exp: 'optional',

      damage: 'optional',
      breath: 'optional',
      blood: 'optional',

      exclude: 'optional',

      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional',

      item_id: 'optional',
      art_id: 'optional',
      parent_id: 'optional'
    }) as AttackCreateParameter['data']

    if ([item_id, art_id].filter(i => !!i).length !== 1) {
      throw new ValidationError({ message: "Require unique key: item_id, art_id or parent_id" })
    }

    if (!isUniqueAttackByName({
      attacks: await where({ guild_id }),
      name: name,
      art_id: art_id ?? null,
      item_id: item_id ?? null,
      parent_id: parent_id ?? null
    })) {
      const error = errors['attack.alreadyexists']

      console.log('aqui')

      throw error(guild_id, name);
    }

    try {
      const prisma = await session.create({
        data: {
          guild_id: guild_id,
          item_id: item_id,
          art_id: art_id,
          parent_id: parent_id,

          name: name,
          id: uuid(),

          required_exp: required_exp,
          damage: damage,
          breath: breath,
          blood: blood,

          exclude: exclude ? 'true' : 'false',

          embed_title: embed_title,
          embed_description: embed_description,
          embed_url: embed_url
        }
      })

      const attack = format(prisma)
      
      database.notify<AttackNotifyType, Attack>({ type: 'attack.create', data: attack })

      return attack;
    } catch (err) {
      const error = geterr(err, { guild_id, art_id, item_id, parent_id })

      throw error();
    }
  } // Function: Anonymous ({ guild_id, id })
} // Function: createAttack

export default createAttack;