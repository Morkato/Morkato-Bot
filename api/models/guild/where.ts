import type { GuildWhereFunction } from 'type:models/guild'
import type { Database } from 'type:models/database'

import { format } from 'utils/guild'

export function whereGuild(database: Database): GuildWhereFunction {
  const session = database.session.guild

  return async ({  }) => {
    const guilds = await session.findMany({
      where: {  }
    })

    return guilds.map(format);
  } // Function: Anonymous ({  })
} // Function: whereGuild

export default whereGuild;