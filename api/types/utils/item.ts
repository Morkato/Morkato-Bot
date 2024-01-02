import type { Item } from '../models/item'

export type IsUniqueItemByNameParameter = { name: string, id?: string, items: Item[] }