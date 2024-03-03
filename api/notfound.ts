import type { Request, Response } from "express"

export default (req: Request, res: Response) => {
  res.status(404).json({ "message": "Opps! Você encontrou algo que não existe." })
}