require('dotenv').config();

module.exports = {
  serverRuntimeConfig: {
    port: process.env.NEXT_PUBLIC_WEBSERVER_PORT || 5500
  }
}
