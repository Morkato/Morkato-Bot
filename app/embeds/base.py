from morkbmt.msgbuilder import MessageBuilder
from morkbmt.embeds import EmbedBuilder

class BaseEmbedBuilder(EmbedBuilder):
  CHUNK_SIZE: int
  LANGUAGE: str
  DEFAULT_ICON: str
  msgbuilder: MessageBuilder
  @classmethod
  def setup(cls, builder: MessageBuilder, icon: str) -> None:
    cls.LANGUAGE = builder.PT_BR
    cls.DEFAULT_ICON = icon
    cls.msgbuilder = builder
    cls.CHUNK_SIZE = 25