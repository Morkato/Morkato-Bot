from morkato.work.bot import MorkatoBot
from morkato.state import MorkatoConnectionState
from morkato.http import HTTPClient
from typing_extensions import Self
from discord import ClientUser
from typing import Iterable
from glob import glob

class AppBot(MorkatoBot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.morkato_http: HTTPClient = HTTPClient(self.loop)
    self.morkato_connection: MorkatoConnectionState = MorkatoConnectionState(self.dispatch, http=self.morkato_http)
  async def __aenter__(self) -> Self:
    await super().__aenter__()
    await self.morkato_http.static_login()
    return self
  async def __aexit__(self, *args) -> None:
    await super().__aexit__(*args)
    await self.morkato_http.close()
  async def _async_setup_hook(self) -> None:
    await super()._async_setup_hook()
    self.morkato_http.loop = self.loop
  async def setup_hook(self):
    self.inject(MorkatoConnectionState, self.morkato_connection)
    self.inject(HTTPClient, self.morkato_http)
    self.inject(ClientUser, self.user)
    unloaded_extensions: Iterable[str] = glob("app/extensions/*.py") + glob("app/converters/*.py")
    unloaded_extensions = (uex[:-3].replace('/', '.') for uex in unloaded_extensions)
    for name in unloaded_extensions:
      await self.load_morkato_extension(name)