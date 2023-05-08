import { getLanguage } from 'languages'

export default async ({params}: {
  children: React.ReactNode
  params: { lang: 'en' | 'pt-BR' }
}) => {
  return (
    <>
      <pre>a</pre>
    </>
  )
}