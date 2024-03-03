import type { Attack, AttackNotifyType, AttackEditFunction, AttackEditParameter } from "type:models/attack"
import type { Database, EditData } from "type:models/database"

import { prismaError, errors } from "errors/prisma"
import { assert, schemas } from 'utils/schema'
import { format } from "utils/attack"

import { validate } from 'schemas'
import { stripAll } from "utils/string"

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

export function editAttack(database: Database): AttackEditFunction {
  const session = database.session.attack

  return async ({ guild_id, id, data }) => {
    guild_id = assert(schemas.id, guild_id)
    id       = assert(schemas.id,       id)
    
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
      embed_url
    } = validate(data, {
      name: 'optional',
      
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
      embed_url: 'optional'
    }) as AttackEditParameter['data']

    const before = await database.getAttack({ guild_id, id })
    let key: string | undefined = undefined
    
    if (before && name && stripAll(name) !== stripAll(before.name)) {
      const art = await database.getArt({ guild_id, id: before.art_id })

      key = art.type === 'FIGHTING_STYLE' ? art.id + ':' + stripAll(name) : stripAll(name)
    }

    let guildHasCreated = false

    async function execute() {
      try {
        const prisma = await session.update({
          where: { guild_id_id: { guild_id, id } },
          data: {
            key: key,
            name: name,
            
            title: title,
            description: description,
            banner: banner,
  
            damage: damage,
            breath: breath,
            blood: blood,
  
            exclude: exclude === undefined ? undefined : exclude ? 'true' : 'false',
            intents: intents,
            created_by: created_by,
  
            embed_title: embed_title,
            embed_description: embed_description,
            embed_url: embed_url,
  
            updated_at: new Date()
          }
        })
  
        const after = format(prisma)
        
        database.notify<AttackNotifyType, EditData<Attack>>({ type: 'attack.edit', data: { before, after } })
  
        return after;
      } catch (err) {
        const type = prismaError(err)

        if (type === 'guild.notfound' && !guildHasCreated) {
          await database.createGuild({ data: { id: guild_id } })
          guildHasCreated = true
          return await execute();
        }

        const error = geterr(type, { guild_id, art_id: before.art_id, parent_id: before.parent_id })
  
        throw error();
      }
    }

    return await execute();
  } // Function: Anonymous ({ guild_id, id, data })
} // Function: editAttack

export default editAttack;