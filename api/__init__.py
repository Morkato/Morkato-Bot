from .url import Response, Route, session
from decouple import config

TOKEN = config('BOT_TOKEN')

CACHE = {}

URL = Route('/', config('URL'))
API = Route('/api/bot', URL)

GUILDS = Route('/guilds', API)
GUILD_ID = Route('/$guild_id', GUILDS)

ARTS = Route('/arts', GUILD_ID)
ART = Route('/$art_name', ARTS)

def format(route: Route, /, **kwargs) -> Route:
  return route.format(**kwargs)
