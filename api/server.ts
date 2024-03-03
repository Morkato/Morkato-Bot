import prepareApp from 'app'

const runApp = prepareApp()

const app = runApp((logger) => {
  logger.info("Server has listening...")
})