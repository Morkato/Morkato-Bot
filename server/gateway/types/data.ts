import type { WebSocketOP } from './operators'
import type { Events } from './events'

import type { User } from "morkato/config"

export type ReadyData = User & { guilds?: any, attacks?: any, arts?: any, players?: any, items?: any, playerItems?: any }

export type WebSocketData<T = any> = {
  op: WebSocketOP
  e?: Events
  d?: T
}