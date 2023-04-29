import { getGuildsByBearerToken } from '@/morkato/bot'
import { NextApiRequest, NextApiResponse } from "next"

const methods = Object.freeze({
  async GET(req: NextApiRequest, res: NextApiResponse) {
    if (!req.headers.authorization) {
      res.status(403).json({ error: '403: Você não possui permissão para execultar essa ação.', action: 'Verifique se você tem permissão para execultar essa ação.', status: 403 })

      return
    }

    try {
      const guilds = await getGuildsByBearerToken(req.headers.authorization)
      
      res.status(200).json(guilds)
    } catch(err) {
      res.status(err.statusCode).json({ error: `${err.statusCode}: ${err.message}`, action: err.action, status: err.statusCode })
    }
  },
  async DEFAULT(req: NextApiRequest, res: NextApiResponse)  {
    res.setHeader('Allow', ['GET'])
    res.status(405).json({ error: '405: MethodNotAllowed', message: `Method: ${req.method} not Allowed`, status: 405 })
  }
})

export default async (req: NextApiRequest, res: NextApiResponse) => {
  await (methods[req.method || 'GET'] || methods.DEFAULT)(req, res)
}