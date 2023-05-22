(async () => {
  (await import('dotenv')).config()
  const { getGuild } = await import('models/guild')
  const fetch = (await import('node-fetch')).default

  
  const response = await fetch('http://localhost:80/api/bot/guilds/971803172056219728/respirations', { method: "PATCH", body: "{\"name\": \"Sol\"}", headers: { authorization: process.env.BOT_TOKEN, "content-type": "application/json" } })

  console.log(await response.json())
})()

// (async () => {
//   (await import('dotenv')).config()

//   const { Logger } = await import('infra/logger')

//   const logger = Logger({
//     app: 'test',
//     forFormat: '$user $app $func $Server $art_type $art_name \n\t$type : $message',
//     registryLog: false
//   })

//   logger.info('Uma mensagem', {functionName: 'async Anonymous', userName: 'V1NI0456:1313' })
// })()