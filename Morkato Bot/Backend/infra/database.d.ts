import { Pool, PoolClient, QueryResult } from 'pg'

declare const cache: { pool: Pool | null };

declare function query(query: string | { text: string, values?: string[] | number[] }): Promise<QueryResult>;
declare function getClientFromPool(): Promise<PoolClient>;

export { query }