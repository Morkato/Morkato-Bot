import { NextApiRequest, NextApiResponse } from "next"
import { readFileSync } from 'fs'

const methods = Object.freeze({
  async GET(req: NextApiRequest, res: NextApiResponse) {
    try {
      const file = readFileSync(`../../../public/styles/${req.query.style}`, { encoding: 'utf-8' }).toString()
  
      res.setHeader('content-type', 'application/stylesheet').send(file)
    } catch {
      res.status(404).json({ error: "404: NotFound", action: "Tente outro nome.", status: 404 })
    }
  },
  async DEFAULT(req: NextApiRequest, res: NextApiResponse) {
    res.setHeader('Allow', ['GET'])
    res.json({ error: '403: MethodNotAllowed', message: `Method: ${req.method} not Allowed`, status: 405 })
  }
})

export default async (req: NextApiRequest, res: NextApiResponse) => {
  await (methods[req.method || 'GET'] || methods.DEFAULT)(req, res)
}