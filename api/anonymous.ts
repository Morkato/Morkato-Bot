import type { User } from "type:users"

const anonymous: User = Object.freeze({
  name: 'anonymous',
  authorization: 'anonymous',
  roles: []
})

export default anonymous;