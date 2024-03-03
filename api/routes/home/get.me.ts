import type { Database } from "type:models/database"
import type { Handler } from 'express'
import type { User } from 'type:users'

import type { Player } from "type:models/player"
import type { Attack } from "type:models/attack"
import type { Guild } from "type:models/guild"
import type { Item } from 'type:models/item'
import type { Art } from "type:models/art"

export default (db: Database): Handler => {
  return async (req, res) => {
    const me: Omit<User, 'authorization'> & {
      guilds?: Record<Guild['id'], {
        arts: Record<Art['id'], Omit<Art, 'guild_id' | 'id'> & { attacks: Record<Attack['id'], Omit<Attack, 'id' | 'guild_id' | 'art_id'>> }>,
        players: Record<Player['id'], Omit<Player, 'guild_id' | 'id'>>
        items: Record<Item['id'], Omit<Item, 'guild_id' | 'id'>>
      }>
    } = { ...req.usr }

    if (req.usr.roles.includes('MANAGE:GUILDS')) {
      const arts = req.usr.roles.includes('MANAGE:ARTS') ? await db.findArt({ }) : []
      const attacks = req.usr.roles.includes('MANAGE:ATTACKS') ? await db.findAttack({ }) : []
      const players = req.usr.roles.includes('MANAGE:PLAYERS') ? await db.findPlayer({  }) : []
      const items = req.usr.roles.includes('MANAGE:ITEMS') ? await db.findItem({ }) : []

      const guilds_chunk = await db.findGuild({  })
      const guilds = guilds_chunk.map(guild => {
        const arts_chunk = arts.filter(art => art.guild_id === guild.id)
        const arts_guild = arts_chunk.map(art => {
          const attacks_chunk = attacks.filter(attack => attack.guild_id === art.guild_id && attack.art_id === art.id)
          const attacks_art = attacks_chunk.map(attack => {
            return [attack.id, Object.assign({}, attack, { id: undefined, guild_id: undefined, art_id: undefined })]
          })

          return [art.id, Object.assign({}, art, { id: undefined, guild_id: undefined }, { attacks: Object.fromEntries(attacks_art) })];
        })

        const players_chunk = players.filter(player => player.guild_id === guild.id)
        const items_chunk = items.filter(item => item.guild_id === guild.id)

        const players_guild = players_chunk.map(player => {
          return [player.id, Object.assign({}, player, { id: undefined, guild_id: undefined })]
        })

        const items_guild = items_chunk.map(item => {
          return [item.id, Object.assign({}, item, { id: undefined, guild_id: undefined })]
        })

        return [guild.id, {
          arts: Object.fromEntries(arts_guild),
          players: Object.fromEntries(players_guild),
          items: Object.fromEntries(items_guild)
        }]
      })
      

      me.guilds = Object.fromEntries(guilds)
    }

    (me as any)['authorization'] = undefined

    res.status(200).json(me)
  }
}