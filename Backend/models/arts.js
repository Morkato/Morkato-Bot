const { query } = require('../infra/database')

const { NotFoundError } = require('../erros/index')

const getAll = async () => {
  const expcted = {
    text: `
      SELECT
        *
      FROM
        arts
    ;`
  }

  const resuslts = await query(expcted)

  return resuslts.rows;
}
const getAllFromGuild = async (guild_id) => {
  const expcted = {
    text: `
      SELECT
        *
      FROM
        arts
      WHERE
        guild_id = $1
    ;`,
    values: [guild_id]
  }

  const resuslts = await query(expcted)

  return resuslts.rows;
}

const getArtsFromType = async (type) => {
  const expcted = {
    text: `
      SELECT
        *
      FROM
        arts
      WHERE
        type = $1
    ;`,
    values: [type]
  }

  const results = await query(expcted)

  return results.rows;
}

const getArtsFromGuildAndType = async (guild_id, type) => {
  const expcted = {
    text: `
      SELECT
        *
      FROM
        arts
      WHERE
        guild_id = $1
        AND type = $2
    ;`,
    values: [guild_id, type]
  }

  const results = await query(expcted)

  return results.rows;
}

const getArtFromType = async ({ name, guild_id, type }) => {
  const expcted = {
    text: `
      SELECT
        *
      FROM
        arts
      WHERE
        guild_id = $1
        AND LOWER(name) = LOWER($2)
        AND type = $3
      LIMIT
        1
    ;`,
    values: [guild_id, name, type]
  }

  const results = await query(expcted)

  if(results.rowCount === 0)
    throw new NotFoundError({ message: "Art type: " + type + " not exists in guild_id \"" + guild_id + "\"." });

  return results.rows[0];
}

const getRespirations = async () => {
  return await getArtsFromType(1);
}

const getRespiration = async (guild_id, name) => {
  return await getArtFromType({ name, guild_id, type: 1 });
}

const getRespirationsFromGuild = async (guild_id) => {
  return await getArtsFromGuildAndType(guild_id, 1);
}
const getKekkijutsus = async () => {
  return await getArtsFromType(2);
}

const getKekkijutsu = async (guild_id, name) => {
  return await getArtFromType({ guild_id, name, type: 2 });
}

const getKekkijutstsFromGuild = async (guild_id) => {
  return await getArtsFromGuildAndType(guild_id, 2);
}

const createArt = async ({
  name,
  type,
  role = null,

  guild_id,
  
  embed_title = null,
  embed_description = null,
  embed_url = null
}) => {
  const expcted = {
    text: `
      INSERT
        INTO arts (
          name,
          type,
          role,
          guild_id,
          embed_title,
          embed_description,
          embed_url
        ) VALUES (
          $1,
          $2,
          $3,
          $4,
          $5,
          $6,
          $7
        ) RETURNING
          *
    ;`,
    values: [
      name,
      type,
      role,
      guild_id,
      embed_title,
      embed_description,
      embed_url
    ]
  }

  try {
    const results = await query(expcted)

    return results.rows[0];
  } catch(err) {
    throw err;
  }
}

const createRespiration = async ({
  name,
  role = null,

  guild_id,
  
  embed_title = null,
  embed_description = null,
  embed_url = null
}) => {
  return await createArt({
    name: name,
    type: 1,
    role: role,

    guild_id: guild_id,

    embed_title: embed_title,
    embed_description: embed_description,
    embed_url: embed_url
  })
}

const createKekkijutsu = async ({
  name,
  role = null,

  guild_id,
  
  embed_title = null,
  embed_description = null,
  embed_url = null
}) => {
  return await createArt({
    name: name,
    type: 2,
    role: role,

    guild_id: guild_id,

    embed_title: embed_title,
    embed_description: embed_description,
    embed_url: embed_url
  })
}

const editArt = async (art, to) => {
  const [ original_name, type, guild_id ] = [ art.name, art.type, art.guild_id ]
  
  const { name, role, embed_title, embed_description, embed_url } = {...art, ...to}
  
  const expcted = {
    text: `
      UPDATE
        arts
      SET
        name = $2,
        role = $4,

        embed_title = $6,
        embed_description = $7,
        embed_url = $8,

        updated_at = (NOW())
      WHERE
        guild_id = $5
        AND LOWER(name) = LOWER($1)
        AND type = $3
      LIMIT
        1
      RETURNING
        *
    ;`,
    values: [original_name, name, type, role, guild_id, embed_title, embed_description, embed_url]
  }

  const results = await query(expcted)

  return results.rows[0]
}

const editRespiration = async (resp, to) => await editArt({ ...resp, type: 1 }, to)
const editKekkijutsu = async (kekki, to) => await editArt({ ...kekki, type: 2 }, to)

const deleteArt = async ({ guild_id, type, name }) => {
  const expected = {
    text: `
      DELETE FROM
        arts
      WHERE
        guild_id = $1
        AND type = $2
        AND LOWER(name) = LOWER($3)
      LIMIT
        1
    ;`,
    values: [guild_id, type, name]
  }

  await query(expected)
}

const deleteRespiration = async (resp) => await deleteArt({...resp, type: 1})
const deleteKekkijutsu = async (kekki) => await deleteArt({...kekki, type: 2})

module.exports = Object.freeze({
  getAll,
  getAllFromGuild,
  getRespirations,
  getRespiration,
  getRespirationsFromGuild,
  getKekkijutsus,
  getKekkijutsu,
  getKekkijutstsFromGuild,

  createRespiration,
  createKekkijutsu,

  editRespiration,
  editKekkijutsu,

  deleteRespiration,
  deleteKekkijutsu
})