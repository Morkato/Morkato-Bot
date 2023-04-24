const model = require('../models/guild')
const bot = require('./bot')

class Guild {
  constructor(guild) {
    this.id = guild.id
    this.created_at = guild.created_at
    this.updated_at = guild.updated_at
  }
}

const getGuild = async (id) => new Guild(await model.getGuild(id))

module.exports = Object.freeze({
  Guild,

  getGuild
})