(async () => {
  (await import('dotenv')).config()
  const { getRespirationsFromGuild, getRespiration, createRespiration, editRespiration } = await import('models/arts')
  const { getGuild } = await import('models/guild')

  const guild = await getGuild('971803172056219728')
  const resp = await getRespiration(guild.id, "Água")
  
  console.log(resp)

  const editedResp = await editRespiration(resp, {
    embed_title: "Respiração: $name Pudim"
  })

  console.log(editedResp)



// //   // console.log(await getGuild('1030300817175089203'))

//   const language = await getLanguage('pt-BR', '/')

//   const format = {
//     test: "AYooooo",
//     user: "Anonymous"
//   }
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