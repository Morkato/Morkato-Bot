interface UserTokenResponse {
  access_token: string
  token_type: string
  expires_in: number
  refresh_token: string
  scope: string
}

const extractCode = async (code: string): Promise<UserTokenResponse | null> => {
  const data = new URLSearchParams()
  
  data.append('client_id', process.env.CLIENT_ID)
  data.append('client_secret', process.env.CLIENT_SECRET)
  data.append('grant_type', 'authorization_code')
  data.append('code', code)
  data.append('redirect_uri', process.env.URL + '/api/oauth2')

  const headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  const response = await fetch('https://discord.com/api/oauth2/token', { method: 'POST', headers: headers, body: data })  

  return response.status === 200 ? await response.json() : null;
}

const refreshToken = async (refresh_token: string): Promise<UserTokenResponse | null> => {
  const data = new URLSearchParams()
  
  data.append('client_id', process.env.CLIENT_ID)
  data.append('client_secret', process.env.CLIENT_SECRET)
  data.append('grant_type', 'refresh_token')
  data.append('refresh_token', refresh_token)

  const headers = {
    'content-type': 'application/x-www-form-urlencoded'
  }

  const response = await fetch('https://discord.com/api/oauth2/token', { method: 'POST', headers: headers, body: data })

  return response.status === 200 ? await response.json() : null;
}

const getUserResponse = async (token: string): Promise<Response> => {
  return (await fetch('https://discord.com/api/v9/users/@me', { headers: { authorization: `Bearer ${token}` } }));
}

export default Object.freeze({
  extractCode,
  getUserResponse,
  refreshToken
})

/*
const extractCode = async (code: string) => {
  const data = new URLSearchParams()
  
  data.append('client_id', process.env.CLIENT_ID)
  data.append('client_secret', process.env.CLIENT_SECRET)
  data.append('grant_type', 'authorization_code')
  data.append('code', code)
  data.append('redirect_uri', process.env.REDIRECT_URL + '/api/oauth2')

  const headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }

  const response = await fetch('https://discord.com/api/oauth2/token', { method: 'POST', headers: headers, body: data })  

  return response.status === 200 ? await response.json() : null;
}

const refreshToken = async (refresh_token: string) => {
  const data = new URLSearchParams()
  
  data.append('client_id', process.env.CLIENT_ID)
  data.append('client_secret', process.env.CLIENT_SECRET)
  data.append('grant_type', 'refresh_token')
  data.append('refresh_token', refresh_token)

  const headers = {
    'content-type': 'application/x-www-form-urlencoded'
  }

  const response = await fetch('https://discord.com/api/oauth2/token', { method: 'POST', headers: headers, body: data })

  return response.status === 200 ? await response.json() : null;
}

const getUserResponse = async (token: string) => {
  return (await fetch('https://discord.com/api/v9/users/@me', { headers: { authorization: `Bearer ${token}` } }));
}

export default Object.freeze({
  extractCode,
  getUserResponse,
  refreshToken
})
*/