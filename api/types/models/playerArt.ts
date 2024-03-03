export type PlayerArt = {
  guild_id: string
  player_id: string
  art_id: string

  created_at: number
}

export type PlayerArtWhereParameter = Partial<Omit<PlayerArt, 'created_at'>>
export type PlayerArtGetherParameter = Omit<PlayerArt, 'created_at'>
export type PlayerArtCreateParameter = Omit<PlayerArt, 'created_at'>
export type PlayerArtDeleteParameter = PlayerArtGetherParameter

export type PlayerArtWhereFunction = ({ guild_id, player_id, art_id }: PlayerArtWhereParameter) => Promise<PlayerArt[]>
export type PlayerArtGetherFunction = ({ guild_id, player_id, art_id }: PlayerArtGetherParameter) => Promise<PlayerArt>
export type PlayerArtCreateFunction = ({ guild_id, player_id, art_id }: PlayerArtCreateParameter) => Promise<PlayerArt>
export type PlayerArtDeleteFunction = ({ guild_id, player_id, art_id }: PlayerArtDeleteParameter) => Promise<PlayerArt>

export type PlayerArtDatabase = {
  findPlayerArt: PlayerArtWhereFunction
  getPlayerArt: PlayerArtGetherFunction
  createPlayerArt: PlayerArtCreateFunction
  delPlayerArt: PlayerArtDeleteFunction
}

export type PlayerArtNotifyType =
  | 'player-art.create'
  | 'player-art.delete'