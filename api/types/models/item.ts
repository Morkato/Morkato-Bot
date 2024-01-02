export type Item = {
  guild_id: string
  id: string

  name: string

  description: string | null

  stack: number
  usable: boolean

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  updated_at: null | number
}

export type ItemWhereParameter = { guild_id?: string }
export type ItemGetherParameter = { guild_id: string, id: string }
export type ItemCreateParameter = { guild_id: string, data: Omit<Partial<Item> & Pick<Item, 'name'>, 'guild_id' | 'id' | 'updated_at'> }
export type ItemEditParameter = { guild_id: string, id: string, data: Omit<Partial<Item>, 'guild_id' | 'id' | 'updated_at'> }
export type ItemDeleteParameter = ItemGetherParameter

export type ItemWhereFunction = ({ guild_id }: ItemWhereParameter) => Promise<Item[]>
export type ItemGetherFunction = ({ guild_id, id }: ItemGetherParameter) => Promise<Item>
export type ItemCreateFunction = ({ guild_id, data }: ItemCreateParameter) => Promise<Item>
export type ItemEditFunction = ({ guild_id, id, data }: ItemEditParameter) => Promise<Item>
export type ItemDeleteFunction = ({ guild_id, id }) => Promise<Item>

export type ItemDatabase = {
  where: ItemWhereFunction
  get: ItemGetherFunction
  create: ItemCreateFunction
  edit: ItemEditFunction
  del: ItemDeleteFunction
}

export type ItemNotifyType =
  | 'item.create'
  | 'item.edit'
  | 'item.delete'