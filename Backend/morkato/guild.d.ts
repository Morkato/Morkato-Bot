import type { Guild as typedGuild } from '../models/guild'
import type { Guild as discordGuild } from './bot'

export declare class Guild {
  id: string
  created_at: Date
  updated_at: Date
  
  constructor({ id, created_at, updated_at }: typedGuild);
}

export declare function getGuild(id: string): Promise<Guild>;