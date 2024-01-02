import type { Database, Subscriber } from "type:models/database"

export function notify(observers: Subscriber[]): Database['notify'] {
  return async ({type, data}) => {
    await Promise.all(observers.map(observer => observer({ type, data })))
  };
}