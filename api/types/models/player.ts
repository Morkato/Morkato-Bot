export type PlayerBreed = 'HUMAN' | 'ONI' | 'HYBRID'

export type Player = {
  guild_id: string
  id: string
  breed: PlayerBreed

  name: string
  credibility: number
  history: string | null

  cash: number

  life: number
  blood: number
  breath: number
  exp: number
  force: number
  resistance: number
  velocity: number

  appearance: string | null
  banner: string | null

  updated_at: number | null
}

export type PlayerWhereParameter = Partial<Pick<Player, 'guild_id'>>
export type PlayerGetherParameter = Pick<Player, 'guild_id' | 'id'>
export type PlayerCreateParameter = Pick<PlayerGetherParameter, 'guild_id'> & { data: Omit<Partial<Player>, 'guild_id' | 'updated_at'> & Pick<Player, 'id' | 'name' | 'breed'> }
export type PlayerEditParameter = PlayerGetherParameter & { data: Omit<Partial<Player>, 'guild_id' | 'id' | 'updated_at'> }
export type PlayerDeleteParameter = PlayerGetherParameter

export type PlayerWhereFunction = ({ guild_id }: PlayerWhereParameter) => Promise<Player[]>
export type PlayerGetherFunction = ({ guild_id, id }: PlayerGetherParameter) => Promise<Player>
export type PlayerCreateFunction = ({ guild_id, data }: PlayerCreateParameter) => Promise<Player>
export type PlayerEditFunction = ({ guild_id, id, data }: PlayerEditParameter) => Promise<Player>
export type PlayerDeleteFunction = ({ guild_id, id }: PlayerDeleteParameter) => Promise<Player>

export type PlayerDatabase = {
  where: PlayerWhereFunction
  get: PlayerGetherFunction
  create: PlayerCreateFunction
  edit: PlayerEditFunction
  del: PlayerDeleteFunction
}

export type PlayerNotifyType =
  | 'player.create'
  | 'player.edit'
  | 'player.delete'