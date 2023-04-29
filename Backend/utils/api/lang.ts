const getLang = async (lang: string, path: string): Promise<{ head: { [key: string]: string | undefined }, body: { [key: string]: string | undefined } } | null> => {
  const response = await fetch(`${process.env.URL}/api/lang/${lang}?route=${path}`)

  return response.status === 200 ? await response.json() : null
}

export default Object.freeze({
  getLang
})