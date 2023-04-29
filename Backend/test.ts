import Logger from 'infra/logger'

const logger = Logger({
  appName: 'test',
  errorExit: true,
  format: '$user - $message'
})

logger.warn('Usuário fez uma requição para obtém as respirações.', {
  config: {
    userName: "Anonymous"
  },
  registryLog: true
})