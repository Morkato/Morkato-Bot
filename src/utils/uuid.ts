const range = 1000000000000000000

export function uuid(identify?: string | null) {
  identify = !identify ? identify : identify.toUpperCase()

  const id = parseInt((Math.random() * range).toString()) + Date.now().toString()

  return !identify ? id : `${identify}:${id}`
}