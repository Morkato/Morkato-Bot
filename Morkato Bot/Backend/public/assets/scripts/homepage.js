$(window)
  .ready(async () => {
    const token = localStorage.getItem('bearer_token')

    if(!token) {
      console.log('Sem bearer token')

      return
    }

    const response = await (await fetch('https://discord.com/api/v9/users/@me', { headers: { authorization: 'Bearer ' + token } })).json()

    console.log(response)
  }) 