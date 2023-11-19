import { WebSocketOP } from "./types/operators"
import { Session } from "./types/session"
import { WebSocketData, ReadyData } from "./types/data"

import { hasPermission } from "morkato/config"

import client from 'morkato/infra/database'

import Players from 'models/players'
import PlayerItems from 'models/player_items'
import Attacks from 'models/attacks'
import Guilds from 'models/guild'
import Items from 'models/items'
import Arts from 'models/arts'

const players = Players(client.player, client.playerItem)
const player_items = PlayerItems(client.playerItem)
const attacks = Attacks(client.attack)
const guilds = Guilds(client.guild)
const items = Items(client.item)
const arts = Arts(client.art)

export const ops = Object.freeze({
  [WebSocketOP.HEARTBEAT]: async ({ setLatency, setAlive }: Session, { d }: WebSocketData<number>) => {
    if (!d) { return; }

    setAlive(true)
    setLatency(Date.now() - d)
  },
  [WebSocketOP.IDENTIFY]: async ({ getIdentify, setIdentify, send }: Session, { d }: WebSocketData<string>) => {
    if (!d) return;

    setIdentify(d)

    const usr = getIdentify()

    if (!usr) return;

    const payload: ReadyData = usr

    if (hasPermission(usr, 'MANAGE:GUILDS')) {
      payload['guilds'] = await guilds.where({})
    }

    if (hasPermission(usr, 'MANAGE:ATTACKS')) {
      payload['attacks'] = await attacks.where({})
    }

    if (hasPermission(usr, 'MANAGE:ARTS')) {
      payload['arts'] = await arts.where({})
    }

    if (hasPermission(usr, 'MANAGE:PLAYERS')) {
      payload['players'] = await players.where({})
    }

    if (hasPermission(usr, 'MANAGE:ITEMS')) {
      payload['items'] = await items.where({})
    }

    if (hasPermission(usr, 'MANAGE:PLAYER:ITEMS')) {
      payload['playerItems'] = await player_items.where({})
    }

    send<ReadyData>({ op: WebSocketOP.READY, d: payload })
  }
})

export default ops;

export { WebSocketOP };