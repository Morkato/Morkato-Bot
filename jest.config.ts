import type { Config } from 'jest'

export default (): Config => ({
  preset: 'ts-jest',
  roots: [
    'tests'
  ]
})