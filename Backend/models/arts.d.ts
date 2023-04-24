export interface Art {
  name: string
  type: 0 | 1 | 0
  role: string | null

  guild_id: string

  embed_title: string | null
  embed_description: string | null
  embed_url: string | null

  created_at: Date
  updated_at: Date
}

export interface Respiration extends Art {
  type: 1
}

export interface Kekkijutsu extends Art {
  type: 2
}

export declare function getAll(): Promise<Art[]>;
export declare function getAllFromGuild(guild_id: string): Promise<Art[]>;

export declare function getRespirations(): Promise<Respiration[]>;
export declare function getRespirationsFromGuild(guild_id: string): Promise<Respiration[]>;

export declare function getRespiration(guild_id: string, name: string): Promise<Respiration>;
export declare function getKekkijutsu(guild_id: string, name: string): Promise<Kekkijutsu>;

export declare function getKekkijutsus(): Promise<Kekkijutsu[]>;
export declare function getKekkijutsusFromGuild(guild_id: string): Primise<Kekkijutsu[]>;

export declare function createRespiration({
  name,
  role = null,

  guild_id,
  
  embed_title = null,
  embed_description = null,
  embed_url = null
}: {
  name: string,
  role?: string | null,

  guild_id: string,

  embed_title?: string | null,
  embed_description?: string | null,
  embed_url?: string | null
}): Promise<Respiration>;

export declare function createKekkijutsu({
  name,
  role = null,

  guild_id,
  
  embed_title = null,
  embed_description = null,
  embed_url = null
}: {
  name: string,
  role?: string | null,

  guild_id: string,

  embed_title?: string | null,
  embed_description?: string | null,
  embed_url?: string | null
}): Promise<Kekkijutsu>;

export declare function editRespiration(resp: Respiration, to: {
  name?: string
  role?: string | null

  embed_title?: string | null
  embed_description?: string | null
  embed_url?: string | null
}): Promise<Respiration>;

export declare function editKekkijutsu(kekki: Kekkijutsu, to: {
  name?: string
  role?: string | null

  embed_title?: string | null
  embed_description?: string | null
  embed_url?: string | null
}): Promise<Kekkijutsu>;

export declare function deleteRespiration(resp: Respiration): Promise<void>;
export declare function deleteKekkijutsu(kekki: Kekkijutsu): Promise<void>;