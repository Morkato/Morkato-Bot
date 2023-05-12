import { Client, PoolConfig, QueryResult } from 'pg'

export type QueryParams = string | { text: string, values?: (string | number | string[] | number[])[] }

const configuration: PoolConfig = {
  user: process.env.DATABASE_USER,
  host: process.env.DATABASE_HOST,
  password: process.env.DATABASE_PASSWORD,
  database: process.env.DATABASE_NAME,
  port: Number.parseInt(process.env.DATABASE_PORT)
}

export async function query(query: QueryParams, defaultClient?: Client) {
  const client = defaultClient || await getClient()
  const isClientVirtual = !defaultClient

  try {
    const result = await client.query(query)

    if(isClientVirtual)
      await client.end();

    return result;
  } catch(err) {
    if(isClientVirtual)
      await client.end();

    throw err;
  }
}

async function getClient() {
  const client = new Client(configuration)

  await client.connect()

  return client;
}

export default query;