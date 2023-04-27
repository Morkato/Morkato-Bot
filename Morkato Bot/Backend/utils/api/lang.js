const getLang = async (lang, path) => {
  const response = await fetch(`${process.env.URL}/api/lang/${lang}?route=${path}`)

  console.log(response.status)

  return response.status === 200 ? await response.json() : null
}

module.exports = Object.freeze({
  getLang
})