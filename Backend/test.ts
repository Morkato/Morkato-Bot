(async () => {
  (await import('dotenv')).config()

  const { getRespiration, createRespiration } = await import('models/arts')

  const resp = await getRespiration('1', 'test', { userName: 'V1NI0456:1313' })

  console.log(resp)
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