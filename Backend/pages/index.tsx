import auth from '@/middiwares/ServerProps/auth'

import { UserIcon } from '#/NavBar'

export const getServerSideProps = auth(async (ctx, user) => {
  return { props: { username: user.username || 'Fazer Login', avatar: `https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}?size=96` } }
})

export default (props) => (
  <>
    <UserIcon {...props} />
  </>
)