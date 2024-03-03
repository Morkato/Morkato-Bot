export type Attack = {
  name: string
  id: string

  title: string | null
  description: string | null
  banner: string | null

  damage: number
  breath: number
  blood: number

  exclude: boolean
  intents: number

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  guild_id: string
  art_id: string
  parent_id: string | null

  created_by: string | null
  updated_at: null | number
}

export type AttackWhereParameter = { guild_id?: string, art_id?: string, parent_id?: string }
export type AttackGetherParameter = { guild_id: string, id: string }
export type AttackCreateParameter = { guild_id: string, data: Omit<Partial<Attack> & Pick<Attack, 'name' | 'art_id'>, 'id' | 'guild_id' | 'updated_at'> }
export type AttackEditParameter = AttackGetherParameter & { data: Partial<Omit<AttackCreateParameter['data'], 'art_id' | 'item_id' | 'parent_id'>> }
export type AttackDeleteParameter = AttackGetherParameter

export type AttackWhereFunction = ({ guild_id, art_id, parent_id }: AttackWhereParameter) => Promise<Attack[]>
export type AttackGetherFunction = ({ guild_id, id }: AttackGetherParameter) => Promise<Attack>
export type AttackCreateFunction = ({ guild_id, data }: AttackCreateParameter) => Promise<Attack>
export type AttackEditFunction = ({ guild_id, id, data }: AttackEditParameter) => Promise<Attack>
export type AttackDeleteFunction = ({ guild_id, id }: AttackDeleteParameter) => Promise<Attack>

export type AttackDatabase = {
  findAttack: AttackWhereFunction
  getAttack: AttackGetherFunction
  createAttack: AttackCreateFunction
  editAttack: AttackEditFunction
  delAttack: AttackDeleteFunction
}

export type AttackNotifyType =
  | 'attack.create'
  | 'attack.edit'
  | 'attack.delete'