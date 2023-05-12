import { NotFoundError } from 'erros/index'

import valid, { required } from 'models/validator'

import query from 'infra/database'
import Logger from 'infra/logger'


const logger = Logger({
  app: 'models:arts',
  registryLog: true,
  forFormat: '$user $app $func $Server \n\t$type : $message'
})

export interface Guild {
  id: string

  created_at: Date
  updated_at: Date
}

export const getAll = async (): Promise<Guild[]> => {
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

export async function getGuild(id: string): Promise<Guild> {
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

export async function getGuilds(rows_id: string[]): Promise<Guild[]> {
  const placeholders = rows_id.map((_, i) => `$${i + 1}`).join(', ')
  const expected = {
    text: `
      SELECT
        *
      FROM 
        guilds
      WHERE
        id IN (${placeholders})
      LIMIT 
        $${rows_id.length + 1}
    ;`,
    values: [...rows_id, rows_id.length]
  };

  const results = await query(expected);
  return results.rows;
}

export async function createGuild(guild: { id: string }): Promise<Guild> {
  const { id } = valid<{ id: string }>(guild, {
    id: required()
  })

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

export async function deleteGuild({ id }: Guild): Promise<void> {
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