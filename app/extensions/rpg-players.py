from morkato.work.project import registry
from app.extension import BaseExtension

@registry
class RPGPlayer(BaseExtension):
  LANGUAGE: str
  async def setup(self) -> None:
    self.LANGUAGE = self.builder.PT_BR