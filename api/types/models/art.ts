export type ArtType = "RESPIRATION" | "KEKKIJUTSU" | 'FIGHTING_STYLE'

export type Art = {
  name: string
  type: ArtType
  id: string

  exclude: boolean

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  guild_id: string

  updated_at: null | number
}

export type ArtWhereParameter = { guild_id?: string, type?: ArtType }
export type ArtGetherParameter = { guild_id: string, id: string }
export type ArtCreateParameter = { guild_id: string, data: Omit<Partial<Art> & Pick<Art, 'name' | 'type'>, 'guild_id' | 'id' | 'updated_at'> }
export type ArtEditParameter = { guild_id: string, id: string, data: Omit<Partial<Art>, 'guild_id' | 'id'> }
export type ArtDeleteParameter = ArtGetherParameter

export type ArtWhereFunction = ({ guild_id, type }: ArtWhereParameter) => Promise<Art[]>
export type ArtGetherFunction = ({ guild_id, id }: ArtGetherParameter) => Promise<Art>
export type ArtCreateFunction = ({ guild_id, data }: ArtCreateParameter) => Promise<Art>
export type ArtEditFunction = ({ guild_id, id, data }: ArtEditParameter) => Promise<Art>
export type ArtDeleteFunction = ({ guild_id, id }: ArtDeleteParameter) => Promise<Art>

export type ArtDatabase = {
  where: ArtWhereFunction
  get: ArtGetherFunction
  create: ArtCreateFunction
  edit: ArtEditFunction
  del: ArtDeleteFunction
}

export type ArtNotifyType =
  | 'art.create'
  | 'art.edit'
  | 'art.delete'