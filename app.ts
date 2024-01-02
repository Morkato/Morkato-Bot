// import dotenv from 'dotenv'

// import App from 'morkato/app'

// dotenv.config()

// const app = App(5050)

// app.run(5500)

import prepareApp from 'app'

const app = prepareApp()

app.listen(5500, () => console.log("server running..."))