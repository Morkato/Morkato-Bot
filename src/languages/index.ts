import * as utils from 'utils'

type Route = { variables: Record<string, string>, head:Record<string, string>, body: Record<string, string> }
type Language = { global: Record<string, string>, routes: { [key: string]: Route } }

type LanguagesKey = "en" | "pt-BR"

export function getGenericLanguage(lang: LanguagesKey): (router: string) => Promise<Route> {
  return async (router: string) => {
    const file: Language = await import(`./${lang}.json`)

    const globalVariables = utils.object.map(file.global, ([ key, value ]) => utils.string.format(value, file.global))

    const route = file.routes[router]
    
    const variables = { ...globalVariables, ...route.variables, $: '$' }

    return {
      head: utils.object.map(route.head, ([key, value]) => utils.string.format(value, variables)),
      body: utils.object.map(route.body, ([key, value]) => utils.string.format(value, variables)),
      variables: variables
    };
  }
}

const languages = {
  en: getGenericLanguage('en'),
  "pt-BR": getGenericLanguage('pt-BR')
}

export default async function getLanguage(lang: keyof typeof languages, route: string) {
  const language = languages[lang]

  return await language(route);
}

export { getLanguage };