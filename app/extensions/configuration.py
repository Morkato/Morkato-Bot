from morkato.work.project import registry
from app.embeds.base import BaseEmbedBuilder
from app.extension import BaseExtension

@registry
class MorkatoConfiguration(BaseExtension):
  async def setup(self):
    BaseEmbedBuilder.setup(self.builder, self.user.display_avatar.url)
    self.from_archive("global-error.yml")
    self.from_archive("rpg-commands.yml")
    self.from_archive("rpg-rolls.yml")
    self.from_archive("rpg-guild.yml")
    self.from_archive("rpg-utility.yml")
    self.from_archive("rpg-families-abilities.yml")
    self.from_archive("rpg-arts-attacks.yml")
    self.from_archive("rpg-players.yml")
    self.from_archive("embeds.yml")
    self.from_archive("utility.yml")