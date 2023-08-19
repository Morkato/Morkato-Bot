import dotenv from 'dotenv'

dotenv.config()

describe('Rota /guilds/971803172056219728', () => {
  describe('Usuários Anônimos', () => {
    test('Tentando acessar as informações', async () => {
      const response = await fetch(new URL('/guilds/971803172056219728', process.env.URL))
      const body     = await response.json()

      expect(response.status).toEqual(401)
    })
  })
})