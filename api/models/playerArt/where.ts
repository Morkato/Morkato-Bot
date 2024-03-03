import type { PlayerArtWhereFunction } from 'type:models/playerArt'
import type { Database } from 'type:models/database'

import { assert, schemas } from 'utils/schema'
import { format } from 'utils/playerArt'

export function wherePlayer(database: Database): PlayerArtWhereFunction {
  const session = database.session.playerArt

  return async ({ guild_id, player_id, art_id }) => {
    guild_id =  guild_id === undefined  ? undefined : assert(schemas.id,  guild_id)
    player_id = player_id === undefined ? undefined : assert(schemas.id, player_id)
    art_id =    art_id === undefined    ? undefined : assert(schemas.id,    art_id)

    const players = await session.findMany({
      where: { guild_id, player_id, art_id }
    })

    return players.map(format);
  }
}

export default wherePlayer;