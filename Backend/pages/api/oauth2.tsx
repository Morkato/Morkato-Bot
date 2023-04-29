import { NextApiRequest, NextApiResponse } from "next"
import { extractCode, refreshToken, getUserResponse } from "@/utils/users"

const methods = {
  async GET(req: NextApiRequest, res: NextApiResponse) {
    const redirect_url = process.env.URL || "http://localhost:3000"
    const { code } = req.query
    const { bearer_token, refresh_token } = req.cookies

    if(code && (typeof code) === 'string') {
      // Extraí um bearer token do Discord.

      const resp = await extractCode(code.toString())

      // Caso o token sajá válido, ele salva no client o token.
      
      if(resp) {
        res.setHeader('Set-Cookie', [
          `bearer_token=${resp.access_token}; Path=/; HttpOnly; Secure; Max-Age=${resp.expires_in}`,
          `refresh_token=${resp.refresh_token}; Path=/; HttpOnly; Secure;`
        ])
  
        // Redireciona para uma página.
        
        res.redirect(redirect_url)

        return;
      }
    }

    // Caso existe um bearer toekn e o mesmo seja valido.

    if(bearer_token && (await fetch('https://discord.com/api/v9/users/@me', { headers: { authorization: `Bearer ${bearer_token}` } }))) {
      res.redirect(redirect_url);

      return;
    }

    // Caso existe um refresh token.

    if(refresh_token) {

      // Verifica e atualiza o bearer token.

      const resp = await refreshToken(refresh_token)

      // Manda essas modificações para o cliente.
      
      if(resp) {
        res.setHeader('Set-Cookie', [
          `bearer_token=${resp.access_token}; Path=/; HttpOnly; Secure; Max-Age=${resp.expires_in}`,
          `refresh_token=${resp.refresh_token}; Path=/; HttpOnly; Secure;`
        ])
  
        res.redirect(redirect_url)

        return;
      }
    }

    // Caso não exista nada relacionado ao usuário.

    res.redirect(`https://discord.com/api/oauth2/authorize?client_id=${process.env.CLIENT_ID}&response_type=code&scope=identify+guilds&redirect_uri=${redirect_url}/api/oauth2`)
  },
  async DEFAULT(req: NextApiRequest, res: NextApiResponse) {
    res.setHeader('Allow', ['GET'])
    res.status(405).json({ error: '405: MethodNotAllowed', message: `Method: ${req.method} not Allowed`, status: 405 })
  }
}

export default async (req: NextApiRequest, res: NextApiResponse) => await (methods[req.method || 'GET'] || methods.DEFAULT)(req, res)