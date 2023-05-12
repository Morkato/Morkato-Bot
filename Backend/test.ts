(async () => {
  (await import('dotenv')).config()

  // const nodeF = (await import('node-fetch'))

  // const { Headers } = nodeF
  // const fetch = nodeF.default

  // const headers = new Headers()

  // headers.set('authorization', process.env.BOT_TOKEN)

  // const response = await fetch('http://localhost:3000/api/bot/guilds/971803172056219728/respirations/agua', { headers, method: "POST", body: JSON.stringify({
  //   name: "agua",
  //   role: null,

  //   embed_title: "Test"
  // }) })

  // console.log(''
  //   +  'Status: '
  //   +  response.status
  //   +  '\n'
  //   +  'Body: '
  // )

  // console.log(await response.json())


//   const { getLanguage } = await import('languages')
//   const { utils } = await import('utils')
//   const fetch = (await import('node-fetch')).default
//   const { createGuild, getGuilds, getGuild } = await import('models/guild')

// //   // console.log(await getGuild('1030300817175089203'))

//   const language = await getLanguage('pt-BR', '/')

//   const format = {
//     test: "AYooooo",
//     user: "Anonymous"
//   }

//   const res = await fetch('http://localhost:3000/api/bot/guilds', { headers: {
//     authorization: process.env.BOT_TOKEN
//   }})

//   console.log(res.status)
//   console.log(await res.json())
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