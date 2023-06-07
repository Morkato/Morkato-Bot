import AttacksFields from 'base:models/fields'
import Guilds from 'models/guild'
import Arts from 'models/arts'

import client from 'infra/database'

const fields = AttacksFields(client.attackField)
const guilds = Guilds(client.guild)
const arts = Arts(client.art)

async function main() {
  const guild = await guilds.getGuild('971803172056219728')
  const artss = await arts.getArts(guild)

  for(let art of artss) {
    for(let attack of art.attacks) {
      await fields.createField({ guild, attack, data: { text: '**•「❤️」$damage de Dano**', roles:[] } })
    }
  }
  
  console.log('Tudo certo.')

  return 0
}

main().then(exit => process.exit(exit))