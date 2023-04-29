import { GetServerSideProps, GetServerSidePropsContext, GetServerSidePropsResult } from 'next'
import { getUserResponse } from '@/utils/users'

export type User = {
  id: string
  username: string
  discriminator: string
  avatar: string
  bot?: boolean
  system?: boolean
  mfa_enebled?: boolean
  banner?: string
  accent_color: number
  locale?: string
  verified?: boolean
  email?: string
  flags?: number
}

export type CustomServerSideProps<
  Props extends { [key: string]: any } = { [key: string]: any }
> = (context: GetServerSidePropsContext, user: User | null) => Promise<GetServerSidePropsResult<Props>>

export default (handle: CustomServerSideProps): GetServerSideProps => {
  return async (context: GetServerSidePropsContext) => {
    const { req, res } = context

    const token = req.cookies['bearer_token']
    
    if(!token) return await handle(context, null)
    
    const response = await getUserResponse(token)

    if(!(response.status === 200)) return await handle(context, null)
    
    return await handle(context, await response.json())
  }
}