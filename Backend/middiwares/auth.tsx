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
> = (context: GetServerSidePropsContext, user?: User) => Promise<GetServerSidePropsResult<Props>>

export default (handle: CustomServerSideProps, ifnotToken?: GetServerSideProps): GetServerSideProps => {
  return async (context: GetServerSidePropsContext) => {
    const { req, res } = context

    const token = req.cookies['bearer_token']
    
    if(!token) return !ifnotToken ? { props: { token_valid: false } } : await ifnotToken(context);
    
    const response = await getUserResponse(token)

    if(!(response.status === 200)) return !ifnotToken ? { props: { token_valid: false } } : await ifnotToken(context);
    
    console.log(token)
    return await (handle.length === 2 ? handle(context, await response.json()) : handle(context));
  }
}