import { type NextRequest, NextResponse } from "next/server"

export const GET = (req: NextRequest) => {
  return NextResponse.json({ ayo: "Guilds", status: "ok" })
}