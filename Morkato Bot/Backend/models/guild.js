const { query } = require('../infra/database')

const { NotFoundError } = ('../erros/index')

const getAll = async () => {
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

const getGuild = async (id) => {
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

const getGuilds = async (rows_id) => {
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

const createGuild = async ({ id }) => {
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

const deleteGuild = async ({ id }) => {
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

module.exports = Object.freeze({
  getAll,
  getGuilds,
  getGuild,

  createGuild,

  deleteGuild
})