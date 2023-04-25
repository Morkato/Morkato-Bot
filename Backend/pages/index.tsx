import auth from '@/middiwares/auth'
import { Head } from '#/Head'

export const getServerSideProps = auth(async (ctx, user) => {
  return { props: { username: user.username, image: `https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}` } }
})

export default ({ image, username, token_valid }) => {
  return (
    <>
      <Head links={[{
        rel: "stylesheet",
        href: "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
        integrity: "sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3",
        crossorigin: "anonymous"
      }]} scripts={[{
        src: "https://code.jquery.com/jquery-3.6.4.js",
        crossorigin: "anonymous",
        integrity: "jBBRygX1Bh5lt8GZjXDzyOB+bWve9EiO7tROUtj/E='."
      }, {
        src: "/desktop/scripts/homepage.js"
      }]} />
    
      <nav className='navbar'>
        <div className='user-info'>
          <span>{username}</span>
          <img src={`${image}?size=64`} alt={`${username}`} />
        </div>
      </nav>
    </>
  )
}