export interface Guild {
  id: string
  name: string
  icon: string | null
  owner: boolean
  permissions: string
  features: any[]
}

export declare function getGuilds(): Promise<Guild[]>;
export declare function getGuild(id: string): Promise<Guild | undefined>;

export declare function getGuildsByBearerToken(bearer_token: string): Promise<Guild[]>