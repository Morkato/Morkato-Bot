import { respiration } from 'middlewares/bot/database'
import { editRespiration } from 'models/arts'
import { NextResponse } from 'next/server'

export default respiration(async (req, ctx, respiration) => {
  return NextResponse.json(respiration);
});

export const POST = respiration(async (req, { params }, respiration) => {
  const editedRespiration = await editRespiration(respiration, await req.json())

  return NextResponse.json(editedRespiration)
})
