export interface Guild {
  id: string

  created_at: Date
  updated_at: Date
}

export declare function getAll(): Promise<Guild[]>;
export declare function getGuilds(rows_id: string[]): Promise<Guild[]>;
export declare function getGuild(id: string): Promise<Guild>;

export declare function createGuild({ id }: { id: string }): Promise<Guild>;

export declare function deleteGuild({ id }: Guild): Promise<void>;