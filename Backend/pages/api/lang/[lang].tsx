import { NextApiRequest, NextApiResponse } from 'next'

import lang from '@/lang.json'

const methods = {
  async GET(req: NextApiRequest, res: NextApiResponse) {
    const { route } = req.query

    if(!route) {
      res.status(400).json({ error: '400: BadRequest', message: "Param: route is required.", status: 400 })

      return;
    }

    else if(route instanceof Array<String>) {
      res.status(400).json({ error: '400: BadRequest', message: "Param: route it must be string.", status: 400 })

      return;
    }

    const language = lang[route][req.query.lang]

    res.status(language ? 200 : 404).json(language ? language : { error: "404: LanguageNotExists", message: `Language: ${req.query.lang} not exists, then language "en"`, staus: 404 })
  },
  async DEFAULT(req: NextApiRequest, res: NextApiResponse) {
    res.setHeader('Allow', ['GET'])

    res.status(405).json({ error: '405: MethodNotAllowed', message: `Method: ${req.method} not Allowed`, status: 405 })
  }
}

export default async (req: NextApiRequest, res: NextApiResponse) => {
  return await (methods[req.method || 'GET'] || methods.DEFAULT)(req, res)
}