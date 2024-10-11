from morkato.work.project import registry
from app.extension import BaseExtension
from app.embeds import BaseEmbedBuilder

@registry
class MorkatoConfiguration(BaseExtension):
  async def setup(self):
    BaseEmbedBuilder.set_message_builder(self.builder)
    self.from_archive("global-error.yml")
    self.from_archive("rpg-commands.yml")
    self.from_archive("rpg-utility.yml")
    self.from_archive("rpg-families-abilities.yml")
    self.from_archive("utility.yml")