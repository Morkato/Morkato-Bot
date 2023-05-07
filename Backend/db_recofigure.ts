(async () => {
  (await import('dotenv')).config()

  const { readFile } = await import('fs/promises')
  const { query } = await import('infra/database')
  const { Logger } = await import('infra/logger')

  const logger = Logger({
    app: 'db_reconfigure',
    forFormat: '$date $app $type : $message'
  })

  const db_buffer = await readFile('database.sql', { encoding: 'utf-8' })
  const db_template = db_buffer.toString()

  try {
    await query({ text: db_template })

    logger.info('Sucesso ao reconfigurar o Banco de dados.')
  } catch(err) {
    logger.error('Erro ao reconfigurar o Banco de dados. Tente ver se tem algo de errado no arquivo "database.sql"', { error: err })

    return;
  }
})()