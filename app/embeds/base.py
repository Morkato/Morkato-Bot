from morkato.work.builder import MessageBuilder
from morkato.work.embeds import EmbedBuilder

class BaseEmbedBuilder(EmbedBuilder):
  CHUNK_SIZE: int
  LANGUAGE: str
  DEFAULT_ICON: str
  builder: MessageBuilder
  @classmethod
  def setup(cls, builder: MessageBuilder, icon: str) -> None:
    cls.LANGUAGE = builder.PT_BR
    cls.DEFAULT_ICON = icon
    cls.builder = builder
    cls.CHUNK_SIZE = 10