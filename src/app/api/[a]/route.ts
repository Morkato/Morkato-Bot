import { NextResponse } from 'next/server'

export const GET = async (req, { params: { a } }) => {
  return NextResponse.json({ c: a })
}