import { WebSocketOperator } from 'type:gateway/operator'
import { WebSocketEvent } from 'type:gateway/event'

export type WebSocketData<T = any> = {
  op: WebSocketOperator
  e?: WebSocketEvent
  d?: T
}