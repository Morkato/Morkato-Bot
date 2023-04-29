const defautHeader = { authorization: process.env.TEST_BEARER_TOKEN }

describe("GET /api/v1/guilds", () => {
  describe('Usuário não autenticado', () => {
    test('Usuário tentando ter acesso aos servidores', async () => {
      const response = await fetch('http://localhost:3000/api/v1/guilds')
      const responseBody = await response.json()

      expect(response.status).toEqual(403)
      expect(responseBody.status).toEqual(403)
      expect(responseBody.error).toEqual('403: Você não possui permissão para execultar essa ação.')
      expect(responseBody.action).toEqual('Verifique se você tem permissão para execultar essa ação.')
    })
  })
  describe('Usuário com Bearer token tentando ter acesso ao servodores', () => {
    test('Usuário com bearer token valido', async () => {
      const response = await fetch('http://localhost:3000/api/v1/guilds', { headers: defautHeader })
      
      expect(response.status).toEqual(200)
    })

    test('Usuário com bearer token invalido', async () => {
      const response = await fetch('http://localhost:3000/api/v1/guilds', { headers: { authorization: 'a ' } })
      const responseBody = await response.json()

      expect(response.status).toEqual(401)
      expect(responseBody.error).toEqual('401: Esse bearer token é invalido.')
      expect(responseBody.action).toEqual('Insira um bearer token valido.')
      expect(responseBody.status).toEqual(401)
    })
  })
})