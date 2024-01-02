import prepareApp from './app'

const app = prepareApp()

app.listen(5500, () => console.log("server running..."))