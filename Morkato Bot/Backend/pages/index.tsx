import auth from '@/middiwares/ServerProps/auth'
import { getLang } from '@/utils/api/lang'
import { useState } from 'react'
import { Head } from '#/Head'

export const getServerSideProps = auth(async (ctx, user) => {
  const lang = await getLang(ctx.locale || 'en', ctx.resolvedUrl)

  if(lang['error'])
    return {
      redirect: {
        basePath: '/en',
        permanent: true
      },
      props: {}
    };

  if(user)
    return { props: { lang: lang, name: user.username, image: `https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}`, is_user: true } };
  return { props: { lang, name: lang.body.login, image: "/desktop/notlogin.jpg", is_user: false } }
})

export default ({ lang, name, image, is_user }) => {
  const onCliickLogin = () => window.location.href = `/api/oauth2`
  const onClickDashboard = () => window.location.href = `/dashboard`

  if(!is_user)
    return (
    <>
      <Head title={lang.head.title} description={lang.head.description} type={lang.head.type}/>

      <Colors />
      <HomePage />

      <div className='bar'>
        <div className='top'>
          
        </div>
        <div className='bottom'>
          <div className='login-area' onClick={onCliickLogin}>
            <img src={`${image}?size=32` } width={32}  height={32} alt={name} />
            <span>{name}</span>
          </div>  
        </div>
      </div>
    </>
  );
  
  const [ dynamicName, setUsername ] = useState('')

  const onHover = () => setUsername(name)
  const onOut = () => setUsername('')

  return (
    <>
      <Head title={lang.head.title} description={lang.head.description} type={lang.head.type}/>

      <Colors />
      <HomePage />

      <div className='bar'>
        <div className='top'>
          <button>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" className="bi bi-house" viewBox="0 0 16 16"> <path fill-rule="evenodd" d="M2 13.5V7h1v6.5a.5.5 0 0 0 .5.5h9a.5.5 0 0 0 .5-.5V7h1v6.5a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 13.5zm11-11V6l-2-2V2.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5z"/> <path fill-rule="evenodd" d="M7.293 1.5a1 1 0 0 1 1.414 0l6.647 6.646a.5.5 0 0 1-.708.708L8 2.207 1.354 8.854a.5.5 0 1 1-.708-.708L7.293 1.5z"/></svg>
            
          </button>
        </div>
        <div className='bottom'>
          <button className='user-info' onClick={onClickDashboard} onMouseOver={onHover} onMouseOut={onOut}>
            <img src={`${image}?size=32` } width={32} height={32} alt={name} />
            <span>{dynamicName}</span>
          </button>
        </div>
      </div>
    </>
  )
}

