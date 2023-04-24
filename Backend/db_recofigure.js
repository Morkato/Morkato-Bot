(async () => {
  require('dotenv').config()
  
  const { query } = require('./infra/database')
  const { readFileSync } = require('fs')

  const database = readFileSync('database.sql', { encoding: 'utf-8' }).toString()

  try {await query({ text: database })}
  catch(err) { console.error(err) }
})()