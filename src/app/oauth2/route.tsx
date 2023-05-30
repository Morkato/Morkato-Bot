import type { NextRequest } from 'next/server'

import { extractCode, refreshToken } from 'utils/users'
import { NextResponse } from 'next/server'

const day = 24 * 60 * 60 

export async function GET(req: NextRequest) {
  const [ redirect_url, code ] = [ req.nextUrl.searchParams.get('redirect_url') || ' /', req.nextUrl.searchParams.get('code') ]
  const [ bearer_token, refresh_token ] = [ req.cookies.get('bearer_token')?.value, req.cookies.get('refresh_token')?.value ]

  const { origin } = req.nextUrl

  const headers = new Headers()

  if(code && (typeof code) === 'string') {
    // Extraí um bearer token do Discord.

    const resp = await extractCode(code.toString(), new URL('/oauth2', origin))

    // Caso o token sajá válido, ele salva no client o token.
      
    if(resp) {
      const cookies = [
        `bearer_token=${resp.access_token}; Path=/; HttpOnly; Secure; Max-Age=${resp.expires_in}`,
        `refresh_token=${resp.refresh_token}; Path=/; HttpOnly; Secure; Max-Age=${Date.now() + day * 14}`
      ]

      headers.set('Set-Cookie', cookies.join(', '))
        
      return NextResponse.redirect(new URL(redirect_url, origin), { headers });
    }
  }

  // Caso existe um bearer toekn e o mesmo seja valido.

  if(bearer_token && (await fetch('https://discord.com/api/v9/users/@me', { headers: { authorization: `Bearer ${bearer_token}` } }))) {
    return NextResponse.redirect(new URL(redirect_url, origin));
  }

  // Caso existe um refresh token.

  if(refresh_token) {

    // Verifica e atualiza o bearer token.

    const resp = await refreshToken(refresh_token)

    // Manda essas modificações para o cliente.
      
    if(resp) {
      const cookies = [
        `bearer_token=${resp.access_token}; Path=/; HttpOnly; Secure; Max-Age=${resp.expires_in}`,
        `refresh_token=${resp.refresh_token}; Path=/; HttpOnly; Secure; Max-Age=${Date.now() + day * 14}`
      ]

      headers.set('Set-Cookie', cookies.join(', '))

      return NextResponse.redirect(new URL(redirect_url, origin), { headers });
    }
  }

  // Caso não exista nada relacionado ao usuário.

  return NextResponse.redirect(new URL(''
  +  '/api/oauth2/authorize'
  +  `?client_id=${process.env.CLIENT_ID}`
  +  `&response_type=code`
  +  `&scope=identify+guilds`
  +  `&redirect_uri=${new URL('/oauth2', origin)}`,
  'https://discord.com'
  ))
}