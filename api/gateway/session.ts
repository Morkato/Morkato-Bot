import type { WebSocketData } from "type:gateway/data"
import type { Session } from "type:gateway/session"
import type { User } from "type:users"
import type { WebSocket } from "ws"

import { WebSocketOperator } from "type:gateway/operator"
import users from 'users.json'

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
    const usr = users.find(usr => usr.authorization === user)

    if (!usr) {
      return;
    }

    $identify = usr as User
  }

  function terminate() { ws.terminate(); }

  function send<T = any>(obj: WebSocketData<T>) {
    ws.send(JSON.stringify(obj))
  }
  function ping() {
    send({ op: WebSocketOperator.HEARTBEAT, d: Date.now() })
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