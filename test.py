from decouple import config

import requests

TOKEN = config('BOT_TOKEN')

res = requests.post('http://localhost/api/bot/guilds/971803172056219728/attacks/minamo-giri/fields', headers={ 'authorization': TOKEN }, json={ 'text': '**•「❤️」$damage de Dano**' })

print(res)
print(res.text)