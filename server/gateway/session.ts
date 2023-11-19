import type { Session, WebSocketData } from "./types"
import type { User } from "morkato/config"
import type { WebSocket } from "ws"

import { WebSocketOP } from "./types/operators"

import { users } from "morkato/config"

export function createSession(ws: WebSocket): Session {
  let $latency = Number.POSITIVE_INFINITY
  let $alive = true
  let $identify: User | null = null

  function getLatency() { return $latency; }
  function setLatency(ms: number) { $latency = ms; }

  function getAlive() { return $alive }
  function setAlive(a: boolean) { $alive = a }

  function getIdentify() { return $identify; }
  function setIdentify(user: string) {
    const usr = users[user]

    if (!usr) {
      return;
    }

    $identify = usr
  }

  function terminate() { ws.terminate(); }

  function send<T = any>(obj: WebSocketData<T>) {
    ws.send(JSON.stringify(obj))
  }
  function ping() {
    send({ op: WebSocketOP.HEARTBEAT, d: Date.now() })
  }

  return {
    get ws() { return ws },
    get alive() { return getAlive() },
    get latency() { return getLatency() },
    getLatency,
    setLatency,
    getIdentify,
    setIdentify,
    getAlive,
    setAlive,
    terminate,
    send,
    ping
  }
}