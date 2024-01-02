import type { WebSocketManager, WebSocketManagerOptions } from "@discordjs/ws"
import type { REST, RESTOptions } from "@discordjs/rest"

export type BotOptions = {
  websocket: WebSocketManager
  rest: REST
}

export type CreateBotOptions = WebSocketManagerOptions & RESTOptions & { token: string }