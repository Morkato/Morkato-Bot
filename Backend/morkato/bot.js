const { UnauthorizedError, InternalServerError } = require('../erros/index')

const token = process.env.BOT_TOKEN;

if(!token)
  throw new InternalServerError({ message: 'Configure enviroment file.' })

const defaultHeaders = { authorization: `Bot ${token}` }

const getGuilds = async () => await (await fetch('https://discord.com/api/v9/users/@me/guilds', { headers: defaultHeaders })).json()
const getGuild = async (id) => (await getGuilds()).find(e => e.id === id)
const getGuildsByBearerToken = async (bearer_token) => {
  const response = await fetch('https://discord.com/api/v9/users/@me/guilds', { headers: { authorization: `Bearer ${bearer_token}` } })
  
  if(!(response.status === 200))
    throw new UnauthorizedError({ message: 'Esse bearer token é invalido.', action: 'Insira um bearer token valido.' });
  
  return await response.json()
}

module.exports = Object.freeze({
  getGuilds,
  getGuild,

  getGuildsByBearerToken
})
