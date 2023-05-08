import { Client, PoolConfig, PoolClient, QueryResult } from 'pg'

const configuration: PoolConfig = {
  user: process.env.DATABASE_USER,
  host: process.env.DATABASE_HOST,
  password: process.env.DATABASE_PASSWORD,
  database: process.env.DATABASE_NAME,
  port: Number.parseInt(process.env.DATABASE_PORT)
}

const cache: { pool: Client | null } = {
  pool: null
}

export default async function query(query: string | { text: string, values?: (string | number | string[] | number[])[] }): Promise<QueryResult> {
  const client = await getPoolClient()
  let response = null;

  try {
    response = await client.query(query)
  } catch(err) {
    await client.end()

    throw err;
  }

  await client.end()

  return response;
}


async function getPoolClient(): Promise<Client> {
  if(!cache.pool)
    cache.pool = new Client(configuration);
  
  await cache.pool.connect()
  
  return cache.pool;
}

export { query };