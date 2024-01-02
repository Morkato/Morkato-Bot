/**
 * [Type] Database - Configure models/database
 */

import type { PlayerItemNotifyType } from './playerItem'
import type { PlayerNotifyType } from './player'
import type { AttackNotifyType } from './attack'
import type { GuildNotifyType } from './guild'
import type { ItemNotifyType } from './item'
import type { ArtNotifyType } from './art'

import type { PrismaClient } from '@prisma/client'

export type NotifyType =
  | PlayerItemNotifyType
  | PlayerNotifyType
  | AttackNotifyType
  | GuildNotifyType
  | ItemNotifyType
  | ArtNotifyType

export type SubscriberParameter<
  Type extends NotifyType = NotifyType,
  Data extends unknown = unknown
> = {
  type: Type
  data: Data
}

export type Subscriber<
  Type extends NotifyType = NotifyType,
  Data extends unknown = unknown
> = ({ type, data }: SubscriberParameter<Type, Data>) => Promise<void>

export type Database = {
  session: PrismaClient

  notify<T extends NotifyType, D extends unknown>({ type, data }: SubscriberParameter<T, D>): Promise<void>
  subscribe: (subscriber: Subscriber) => void
}