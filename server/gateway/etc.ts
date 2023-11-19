import type { Session, WebSocketData } from "./types"
import type { Permission } from "morkato/config"

import { hasPermission } from 'morkato/config'

export class EncondeError extends Error { }

export function encode<T = any>(msg: string): WebSocketData<T> {
  try {
    const obj = JSON.parse(msg)

    if (typeof obj == 'object' && obj['op']) {
      return obj;
    }

    throw new EncondeError();
  } catch {
    throw new EncondeError();
  }
}

export function filterClients(clients: Session[], perm: Permission): Session[] {
  return clients.filter(({ getIdentify }) => {
    const usr = getIdentify()

    if (!usr) return false;

    return hasPermission(usr, perm);
  })
}