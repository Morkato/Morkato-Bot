import AttacksFields from 'base:models/fields'
import Guilds from 'models/guild'
import Arts from 'models/arts'

import client from 'infra/database'

import b from './b.json'

async function main() {
  const guild = b[0]

  const id = guild.id

  const arts = guild.arts

  for(let art of arts) {
    for(let attack of art.attacks) {
      await client.attack.create({ data: attack })
    }
  }

  return 0
}

main().then(exit => process.exit(exit))