from decouple import config

import requests

TOKEN = config('BOT_TOKEN')

res = requests.post('http://localhost/api/bot/guilds/971803172056219728/vars', headers={ 'authorization': TOKEN }, json={ 'name': 'test2', 'text': 'Testem da vairávvel :D' })

print(res)
print(res.text)