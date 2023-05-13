from .url import Response, Route, session
from decouple import config

TOKEN = config('BOT_TOKEN')

CACHE = {}

URL = Route('/', "http://localhost:3000")
API = Route('/api/bot', URL)

GUILDS = Route('/guilds', API)
GUILD_ID = Route('/$guild_id', GUILDS)

RESPIRATIONS = Route('/respirations', GUILD_ID)
RESPIRATION_NAME = Route('/$respiration_name', RESPIRATIONS)

KEKIJUTSUS = Route('/kekkijutsus', GUILD_ID)
KEKIJUTSU_NAME = Route('/$kekkijutsu_name', KEKIJUTSUS)

def format(route: Route, /, **kwargs) -> Route:
  return route.format(**kwargs)