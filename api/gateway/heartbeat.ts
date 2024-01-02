import type { Session } from "type:gateway/session"

export default (clients: Session[], tick: number): NodeJS.Timeout => {
  return setInterval(() => {
    clients.filter(client => {
      if (client.getIdentify()  === null) {
        return true;
      } else if (!client.getAlive()) {
        client.terminate()

        return false;
      }

      client.setAlive(false)
      client.ping()

      return true;
    })
  }, tick);
}