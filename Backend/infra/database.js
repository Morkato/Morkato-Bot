const { Pool } = require('pg')

const configuration = {
  user: process.env.DATABASE_USER,
  host: process.env.DATABASE_HOST,
  password: process.env.DATABASE_PASSWORD,
  database: process.env.DATABASE_NAME,
  port: process.env.DATABASE_PORT
}

const cache = {
  pool: null
}

async function query(query) {
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


async function getPoolClient() {
  if(!cache.pool)
    cache.pool = new Pool(configuration);

  return await cache.pool.connect()
}

module.exports = Object.freeze({ query })