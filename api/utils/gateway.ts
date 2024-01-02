import type { WebSocketData } from "type:gateway/data"

export function resolve(data: string): WebSocketData<any> | null {
  try {
    const obj = JSON.parse(data)

    if (typeof obj !== 'object' && obj.op === undefined) {
      return null;
    }

    return obj;
  } catch {
    return null;
  }
}