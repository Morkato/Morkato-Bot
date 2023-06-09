import Guilds from 'models/guild'
import Arts from 'models/arts'

import client from 'infra/database'

import b from '/home/marcus/Downloads/Backup.json'



async function main() {
  const guild = b[0]

  const id = guild.id

  const arts = guild.arts

  for(let {
    name,
    type,
    role,
    key,
    guild_id,
    embed_title,
    embed_description,
    embed_url,

    created_at,
    updated_at,
    attacks
  } of arts) {
    for(let a of attacks) {
      await client.attack.create({ data: a })
    }
  }

  return 0
}

main().then(exit => process.exit(exit))