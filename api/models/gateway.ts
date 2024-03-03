import type { Subscriber } from "type:models/database"
import type { Session } from "type:gateway/session"

import type { Player } from "type:models/player"
import type { Attack } from "type:models/attack"
import type { Guild } from "type:models/guild"
import type { Item } from 'type:models/item'
import type { Art } from 'type:models/art'

import { WebSocketOperator } from "type:gateway/operator"

export function prepareGatewaySubscriber(clients: Session[]): Subscriber {
  return async ({ type, data }) => {
    const event = events[type]

    if (!event) {
      return;
    }

    await event(clients, data);
  }
}

const events: Record<string, (clients: Session[], d: any) => Promise<void>> = Object.freeze({
  "player.create": async (clients, player: Player) => {
    for (const client of clients) {
      const usr = client.getIdentify()

      if (!usr || !usr.roles.includes('MANAGE:PLAYERS')) continue;

      client.send<Player>({
        op: WebSocketOperator.DISPATCH,
        e: 'CREATE_PLAYER',
        d: player
      })
    }
  },
  "player.edit": async (clients, player: { before: Player, after: Player }) => {
    for (const client of clients) {
      const usr = client.getIdentify()

      if (!usr || !usr.roles.includes('MANAGE:PLAYERS')) continue;

      client.send<typeof player>({
        op: WebSocketOperator.DISPATCH,
        e: 'UPDATE_PLAYER',
        d: player
      })
    }
  },
  "player.delete": async (clients, player: Player) => {
    for (const client of clients) {
      const usr = client.getIdentify()

      if (!usr || !usr.roles.includes('MANAGE:PLAYERS')) continue;

      client.send<Player>({
        op: WebSocketOperator.DISPATCH,
        e: 'DELETE_PLAYER',
        d: player
      })
    }
  },
  "guild.create": async (clients, guild: Guild) => {
    for (const client of clients) {
      const usr = client.getIdentify()

      if (!usr || !usr.roles.includes('MANAGE:GUILDS')) continue;

      client.send<Guild>({
        op: WebSocketOperator.DISPATCH,
        e: 'CREATE_GUILD',
        d: guild
      })
    }
  },
  "guild.delete": async (clients, guild: Guild) => {
    for (const client of clients) {
      const usr = client.getIdentify()

      if (!usr || !usr.roles.includes('MANAGE:GUILDS')) continue;

      client.send<Guild>({
        op: WebSocketOperator.DISPATCH,
        e: 'DELETE_GUILD',
        d: guild
      })
    }
  },
  "attack.create": async (clients, attack: Attack) => {
    for (const client of clients) {
      const usr = client.getIdentify()

      if (!usr || !usr.roles.includes('MANAGE:ATTACKS')) continue;

      client.send<Attack>({
        op: WebSocketOperator.DISPATCH,
        e: 'CREATE_ATTACK',
        d: attack
      })
    }
  },
  "attack.edit": async (clients, attack: { before: Attack, after: Attack }) => {
    for (const client of clients) {
      const usr = client.getIdentify()

      if (!usr || !usr.roles.includes('MANAGE:ATTACKS')) continue;

      client.send<typeof attack>({
        op: WebSocketOperator.DISPATCH,
        e: 'UPDATE_ATTACK',
        d: attack
      })
    }
  },
  "attack.delete": async (clients, attack: Attack) => {
    for (const client of clients) {
      const usr = client.getIdentify()

      if (!usr || !usr.roles.includes('MANAGE:ATTACKS')) continue;

      client.send<Attack>({
        op: WebSocketOperator.DISPATCH,
        e: 'DELETE_ATTACK',
        d: attack
      })
    }
  },
  "item.create": async (clients, item: Item) => {
    for (const client of clients) {
      const usr = client.getIdentify()

      if (!usr || !usr.roles.includes('MANAGE:ITEMS')) continue;

      client.send<Item>({
        op: WebSocketOperator.DISPATCH,
        e: 'CREATE_ITEM',
        d: item
      })
    }
  },
  "item.edit": async (clients, item: { before: Item, after: Item }) => {
    for (const client of clients) {
      const usr = client.getIdentify()

      if (!usr || !usr.roles.includes('MANAGE:ITEMS')) continue;

      client.send<typeof item>({
        op: WebSocketOperator.DISPATCH,
        e: 'UPDATE_ITEM',
        d: item
      })
    }
  },
  "item.delete": async (clients, item: Item) => {
    for (const client of clients) {
      const usr = client.getIdentify()

      if (!usr || !usr.roles.includes('MANAGE:ITEMS')) continue;

      client.send<Item>({
        op: WebSocketOperator.DISPATCH,
        e: 'DELETE_ITEM',
        d: item
      })
    }
  },
  "art.create": async (clients, art: Art) => {
    for (const client of clients) {
      const usr = client.getIdentify()

      if (!usr || !usr.roles.includes('MANAGE:ARTS')) continue;

      client.send<Art>({
        op: WebSocketOperator.DISPATCH,
        e: 'CREATE_ART',
        d: art
      })
    }
  },
  "art.edit": async (clients, art: { before: Art, after: Art }) => {
    for (const client of clients) {
      const usr = client.getIdentify()

      if (!usr || !usr.roles.includes('MANAGE:ARTS')) continue;

      client.send<typeof art>({
        op: WebSocketOperator.DISPATCH,
        e: 'UPDATE_ART',
        d: art
      })
    }
  },
  "art.delete": async (clients, art: Art) => {
    for (const client of clients) {
      const usr = client.getIdentify()

      if (!usr || !usr.roles.includes('MANAGE:ARTS')) continue;

      client.send<Art>({
        op: WebSocketOperator.DISPATCH,
        e: 'DELETE_ART',
        d: art
      })
    }
  }
})

export default prepareGatewaySubscriber;