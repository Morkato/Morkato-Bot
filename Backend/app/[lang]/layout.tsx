import { i18n } from 'i18n-config'

import { getLanguage } from 'languages'

export async function generateStaticParams() {
  return i18n.locales.map(locale => ({ lang: locale }));
}

export default async function Layout({
  children,
  params
}: {
  children: React.ReactNode
  params: { lang: 'en' | 'pt-BR' }
}) {
  const lang = await getLanguage(params.lang, '/')

  return (
    <html lang={params.lang}>
      <head>
        <title>{lang.head.title}</title>

        <meta name="og:site_name" key="og:site_name" content={lang.head.site_name||"Morkato Bot"} />
        <meta name="og:type" key="og:type" content="website"/>
        
        <meta name="og:title" key="og:title" content={lang.head.title}/>
      </head>

      <body>
        {children}
      </body>
    </html>
  )
}