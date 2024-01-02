import type { Database, Subscriber } from "type:models/database"

export function subscribe(observers: Subscriber[]): Database['subscribe'] {
  return (observer) => {
    observers.push(observer)
  };
}