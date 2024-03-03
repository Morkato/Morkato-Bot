import type { Attack, AttackNotifyType, AttackCreateFunction, AttackCreateParameter } from "type:models/attack"
import type { Database } from "type:models/database"

import { prismaError, errors } from "errors/prisma"
import { assert, schemas } from 'utils/schema'
import { stripAll } from "utils/string"
import { format } from "utils/attack"
import { validate } from 'schemas'
import { uuid } from "utils/uuid"

function geterr(type: string, {
  guild_id,
  art_id,
  parent_id
}: Pick<Attack, 'guild_id'> & Partial<Pick<Attack, 'name' | 'art_id' | 'parent_id'>>) {
  if (type === 'guild.notfound') {
    return () => errors['guild.notfound'](guild_id);
  } else if (type === 'art.notfound') {
    return () => errors['art.notfound'](guild_id, art_id as string);
  } else if (type === 'attack.notfound') {
    return () => errors['attack.notfound'](guild_id, parent_id as string);
  }

  return () => errors['generic.unknown']("Internal Error", "attack.create");
}

export function createAttack(database: Database): AttackCreateFunction {
  const session = database.session.attack

  return async ({ guild_id, data }) => {
    guild_id = assert(schemas.id, guild_id)

    const {
      name,
      title,
      description,
      banner,
      damage,
      breath,
      blood,
      exclude,
      intents,
      created_by,
      embed_title,
      embed_description,
      embed_url,
      art_id,
      parent_id
    } = validate(data, {
      name: 'required',
      
      title: 'optional',
      description: 'optional',
      banner: 'optional',

      damage: 'optional',
      breath: 'optional',
      blood: 'optional',

      exclude: 'optional',
      intents: 'optional',
      created_by: 'optional',

      embed_title: 'optional',
      embed_description: 'optional',
      embed_url: 'optional',

      art_id: 'required',
      parent_id: 'optional'
    }) as AttackCreateParameter['data']

    const art = await database.getArt({ guild_id, id: art_id })
    const key = art.type === 'FIGHTING_STYLE' ? art.id + ':' + stripAll(name) : stripAll(name)

    let guildHasCreated = false
    
    async function execute() {
      try {
        const prisma = await session.create({
          data: {
            id: uuid(),
            key: key,
            guild_id: guild_id,
            art_id: art_id,
            parent_id: parent_id,
  
            name: name,
            title: title,
            description: description,
            banner: banner,
  
            damage: damage,
            breath: breath,
            blood: blood,
  
            exclude: exclude ? 'true' : 'false',
            intents: intents,
            created_by: created_by,
  
            embed_title: embed_title,
            embed_description: embed_description,
            embed_url: embed_url
          }
        })
  
        const attack = format(prisma)
        
        database.notify<AttackNotifyType, Attack>({ type: 'attack.create', data: attack })
  
        return attack;
      } catch (err) {
        const type = prismaError(err)

        if (type === 'guild.notfound' && !guildHasCreated) {
          await database.createGuild({ data: { id: guild_id } })
          guildHasCreated = true
          return await execute();
        }
        
        const error = geterr(type, { guild_id, art_id, parent_id })
  
        throw error();
      }
    }

    return await execute();
  } // Function: Anonymous ({ guild_id, id })
} // Function: createAttack

export default createAttack;