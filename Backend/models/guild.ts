import { NotFoundError } from '@/erros/index'

import query from '@/infra/database'

export interface Guild {
  id: string

  created_at: Date
  updated_at: Date
}

const getAll = async (): Promise<Guild[]> => {
  const expected = {
    text: `
      SELECT
        *
      FROM
        guilds
    ;`
  }

  const results = await query(expected)

  return results.rows;
}

async function getGuild(id: string): Promise<Guild> {
  const expected = {
    text: `
      SELECT
        *
      FROM
        guilds
      WHERE
        id = $1
      LIMIT
        1
    ;`,
    values: [id]
  }

  const results = await query(expected)

  if (results.rowCount === 0)
    throw new NotFoundError({ message: "Guild ID not found." });
  
  return results.rows[0];
}

async function getGuilds(rows_id: number[]): Promise<Guild[]> {
  const expected = {
    text: `
      SELECT
        *
      FROM
        guilds
      WHERE
        id IN ($1)
      LIMIT
        $2
    ;`,
    values: [rows_id, rows_id.length]
  }

  const results = await query(expected)

  return results.rows;
}

async function createGuild({ id }: { id: string }): Promise<Guild> {
  const expected = {
    text: `
      INSERT INTO
        guilds (id)
      VALUES
        ($1)
      RETURNING
        *
    ;`,
    values: [id]
  }

  const results = await query(expected)

  return results.rows[0];
}

async function deleteGuild({ id }: Guild): Promise<void> {
  const expected = {
    text: `
      DELETE FROM
        guilds
      WHERE
        id = $1
      LIMIT
        1
    ;`,
    values: [id]
  }

  await query(expected)
}

export default Object.freeze({
  getAll,
  getGuilds,
  getGuild,

  createGuild,

  deleteGuild
})