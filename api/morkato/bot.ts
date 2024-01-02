import type { BotOptions } from "type:morkato/bot"

import { Client, GatewayIntentBits, GatewayDispatchEvents } from "@discordjs/core"
import { WebSocketManager } from "@discordjs/ws"
import { REST } from '@discordjs/rest'

export class Bot extends Client {
  readonly websocket: WebSocketManager;
  constructor({ rest, websocket }: BotOptions) {
    super({ rest, gateway: websocket })

    this.websocket = websocket;
  }

  async prepare() {
    await this.websocket.connect();
  }
}

Bot.prototype.on(GatewayDispatchEvents.MessageCreate, async (opts) => {
  opts.api
})