import type { API, GatewayMessageCreateDispatchData } from "@discordjs/core"

export type ContextOptions = { api: API, data: GatewayMessageCreateDispatchData }

export interface ContextConstructor {
  new(): void;
}