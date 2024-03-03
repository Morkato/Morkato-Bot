export type PlayerItem = {
  guild_id: string
  item_id: string
  player_id: string

  stack: number

  created_at: number
}

export type PlayerItemWhereParameter = { guild_id?: PlayerItem['guild_id'], item_id?: PlayerItem['item_id'], player_id?: PlayerItem['player_id'] }
export type PlayerItemGatherParameter = { guild_id: PlayerItem['guild_id'], item_id: PlayerItem['item_id'], player_id: PlayerItem['player_id'] }
export type PlayerItemCreateParameter = Pick<PlayerItemGatherParameter, 'guild_id'> & { data: Partial<Omit<PlayerItem, 'guild_id' | 'created_at'>> & Pick<PlayerItem, 'item_id' | 'player_id'> }
export type PlayerItemEditParameter = PlayerItemGatherParameter & { data: Partial<Omit<PlayerItem, 'created_at' | 'guild_id' | 'item_id' | 'player_id'>> }
export type PlayerItemDeleteParameter = PlayerItemGatherParameter & {  }

export type PlayerItemWhereFunction = ({ guild_id, player_id, item_id }: PlayerItemWhereParameter) => Promise<PlayerItem[]>
export type PlayerItemGetherFunction = ({ guild_id, player_id, item_id }: PlayerItemGatherParameter) => Promise<PlayerItem>
export type PlayerItemCreateFunction = ({ guild_id, data }: PlayerItemCreateParameter) => Promise<PlayerItem>
export type PlayerItemEditFunction = ({ guild_id, player_id, item_id, data }: PlayerItemEditParameter) => Promise<PlayerItem>
export type PlayerItemDeleteFunction = ({ guild_id, player_id, item_id }: PlayerItemDeleteParameter) => Promise<PlayerItem>

export type PlayerItemDatabase = {
  findPlayerItem: PlayerItemWhereFunction
  getPlayerItem: PlayerItemGetherFunction
  createPlayerItem: PlayerItemCreateFunction
  editPlayerItem: PlayerItemEditFunction
  delPlayerItem: PlayerItemDeleteFunction
}

export type PlayerItemNotifyType =
  | 'player-item.create'
  | 'player-item.edit'
  | 'player-item.delete'