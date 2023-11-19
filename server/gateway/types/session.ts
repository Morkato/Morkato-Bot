import type { WebSocketData } from "./data"
import type { User } from "morkato/config"
import type { WebSocket } from "ws"

export type Session = {
  get alive(): boolean
  get ws(): WebSocket
  get latency(): number
  getLatency(): number
  setLatency(ms: number): void
  getIdentify(): User | null
  setIdentify(user: string): void
  getAlive(): boolean
  setAlive(a: boolean): void
  send<T = any>(obj: WebSocketData<T>): void
  terminate(): void
  ping(): void
}