from decouple import config

import requests

TOKEN = config('BOT_TOKEN')

res = requests.get('http://localhost/api/bot/guilds/971803172056219728/attacks/minamo-giri/fields', headers={ 'authorization': TOKEN })

print(res)
print(res.text)