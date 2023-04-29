require('dotenv').config()

const nextJest = require('next/jest')

const customJestConfig = nextJest({
  moduleDirectores: [ 'node_modules', '<rootDir>/' ],
  testTimeout: 60000
})

module.exports = customJestConfig