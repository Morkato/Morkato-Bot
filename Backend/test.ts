import Logger from 'infra/logger'

const logger = Logger({
  app: 'test',
  forFormat: '$app - $message'
})

logger.info('funcionou')