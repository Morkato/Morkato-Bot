/**
 * [Type] Database - Configure models/database
 */

import type { PlayerItemDatabase, PlayerItemNotifyType } from './playerItem'
import type { PlayerArtDatabase, PlayerArtNotifyType } from './playerArt' 
import type { PlayerDatabase, PlayerNotifyType } from './player'
import type { AttackDatabase, AttackNotifyType } from './attack'
import type { GuildDatabase, GuildNotifyType } from './guild'
import type { ItemDatabase, ItemNotifyType } from './item'
import type { ArtDatabase, ArtNotifyType } from './art'

import type { PrismaClient } from '@prisma/client'

export type NotifyType =
  | PlayerItemNotifyType
  | PlayerArtNotifyType
  | PlayerNotifyType
  | AttackNotifyType
  | GuildNotifyType
  | ItemNotifyType
  | ArtNotifyType

export type SubscriberParameter<
  Type extends string = string,
  Data extends unknown = unknown
> = {
  type: Type
  data: Data
}

export type Subscriber<
  Type extends string = string,
  Data extends unknown = unknown
> = ({ type, data }: SubscriberParameter<Type, Data>) => Promise<void>

export type EditData<T extends unknown = unknown> = { before: T, after: T }

export type Database = 
  & PlayerItemDatabase
  & PlayerArtDatabase
  & PlayerDatabase
  & AttackDatabase
  & GuildDatabase
  & ItemDatabase
  & ArtDatabase
  & {
  session: PrismaClient
  observers: Subscriber[]

  notify<T extends string, D extends unknown>({ type, data }: SubscriberParameter<T, D>): Promise<void>
  subscribe: (subscriber: Subscriber) => void
}