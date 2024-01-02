from __future__ import annotations

from typing import (
  TYPE_CHECKING,
  ClassVar,
  Union,
  List
)

if TYPE_CHECKING:
  from morkato.context import MorkatoContext
  from morkato.art import ArtType

  from app.utils.flags import (
    BaseType,
    FlagDataType
  )

from morkato.utils.etc import message_checker, reaction_checker, in_range, fmt
from morkato.art       import Art
from app.utils.flags   import (
  FlagGroup,
  flag
)

__all__ = ('ArtFlagGroup',)

class ArtFlagGroup(FlagGroup):
  SUPPORTED_RESPIRATION_TEXTS: ClassVar[List[str]] = [
    "respiracao",
    "respiration",
    "resp",
    'r'
  ]
  
  SUPPORTED_KEKKIJUTSU_TEXTS: ClassVar[List[str]] = [
    "kekkijutsu",
    "kekki",
    'k'
  ]

  SUPPORTED_FIGHTING_STYLE_TEXTS: ClassVar[List[str]] = [
    "fightstyle",
    "fightingstyle",
    "estilodeluta",
    "estiloluta",
    "fs"
  ]

  CREATE_MESSAGE_IF_TYPE_IS_NONE: ClassVar[str] = "É necessário especificar o tipo da arte, se ela é respiração, kekkijutsu ou estilo de luta valido."
  
  CREATE_MESSAGE_ART_IF_NAME_IS_NONE: ClassVar[str] = "Beleza, irei criar uma arte... Uma arte sem nome? Tá certo isso?"
  CREATE_MESSAGE_ART_IF_HAS_CREATED: ClassVar[str] = "A respiração chamada: **`{art.name}`** foi criada."
  
  CREATE_MESSAGE_RESPIRATION_IF_NAME_IS_NONE: ClassVar[str] = "Beleza, irei criar uma respiração... Uma respiração sem nome? Tá certo isso?"
  CREATE_MESSAGE_RESPIRATION_IF_HAS_CREATED: ClassVar[str] = "A respiração chamada: **`{art.name}`** foi criada."

  CREATE_MESSAGE_KEKKIJUTSU_IF_NAME_IS_NONE: ClassVar[str] = "Beleza, irei criar um kekkijutsu... Um kekkijutsu sem nome? Tá certo isso?"
  CREATE_MESSAGE_KEKKIJUTSU_IF_HAS_CREATED: ClassVar[str] = "O kekkijutsu chamada: **`{art.name}`** foi criado."

  CREATE_MESSAGE_FS_IF_NAME_IS_NONE: ClassVar[str] = "Beleza, irei criar um estilo de luta... Um estilo de luta sem nome? Tá certo isso?"
  CREATE_MESSAGE_FS_IF_HAS_CREATED: ClassVar[str] = "O estilo de luta chamada: **`{art.name}`** foi criado."

  RENAME_MESSAGE_IF_BASE_NAME_IS_NONE: ClassVar[str] = "Hunrum, irei mudar o nome do nada para... Pera, pera, cadê o nome?"
  RENAME_MESSAGE_IF_NAMES_HAS_NONE_NAME: ClassVar[str] = "Beleza, irei trocar o nome **`{name}`** para... Para... Pera, vou trocar para o que?"
  RENAME_MESSAGE_IF_AFTER_NAME_PASS_LIMIT_RANGE: ClassVar[str] = "O nome de uma arte deve ter o mínimo entre 02 à 32 caracteres."
  
  RENAME_MESSAGE_IF_ART_HAS_EDITED_NAME: ClassVar[str] = "O nome da arte chamada: **`{before}`** foi alterado para: **`{after}`**"
  RENAME_MESSAGE_IF_RESPIRATION_HAS_EDITED_NAME: ClassVar[str] = "O nome da respiração chamada: **`{before}`** foi alterado para: **`{after}`**"
  RENAME_MESSAGE_IF_KEKKIJUTSU_HAS_EDITED_NAME: ClassVar[str] = "O nome do kekkijutsu chamado: **`{before}`** foi alterado para: **`{after}`**"
  RENAME_MESSAGE_IF_FS_HAS_EDITED_NAME: ClassVar[str] = "O nome do estilo de luta chamado: **`{before}`** foi alterado para: **`{after}`**"

  EDIT_PREFIXES_DONE: ClassVar[List[str]] = [
    "conclude",
    "done",
    "dn",
    'd'
  ]
  EDIT_PREFIXES_TITLE: ClassVar[List[str]] = [
    "titulo",
    "title",
    "tl",
    't'
  ]

  EDIT_PREFIXES_DESCRIPTION: ClassVar[List[str]] = [
    "descricao",
    "description",
    "desc",
    "dc",
    'd'
  ]

  EDIT_PREFIXES_IMAGE: ClassVar[List[str]] = [
    "imagem",
    "image",
    "img",
    "im",
    'i'
  ]
  
  EDIT_MESSAGE_IF_NAME_IS_NONE: ClassVar[str] = "Beleza, como conseguirei editar uma arte sem nome?"
  EDIT_MESSAGE_IF_TITLE_PASS_LIMIT_CHARS: ClassVar[str] = "O título de ter no mínimo entre 2 à 96 caracteres."
  EDIT_MESSAGE_IF_DESCRIPTION_PASS_LIMIT_CHARS: ClassVar[str] = "A descrição de ter no mínimo entre 2 à 4096 caracteres."
  EDIT_MESSAGE_IF_KWARGS_IS_EMPTY: ClassVar[str] = "Pera, pera, tô ficando doido ou você editou nada?"

  EDIT_MESSAGE_ART_HAS_EDITED: ClassVar[str] = "Tudo certo! Editei a arte chamada: **`{art.name}`** :V"
  EDIT_MESSAGE_RESPIRATION_HAS_EDITED: ClassVar[str] = "Tudo certo! Editei a respiração chamada: **`{art.name}`** :V"
  EDIT_MESSAGE_KEKKIJUTSU_HAS_EDITED: ClassVar[str] = "Tudo certo! Editei o kekkijutsu chamada: **`{art.name}`** :V"
  EDIT_MESSAGE_FS_HAS_EDITED: ClassVar[str] = "Tudo certo! Editei o estilo de luta chamada: **`{art.name}`** :V"

  DELETE_MESSAGE_IF_NAME_IS_NONE: ClassVar[str] = "Beleza, vou deletar, deletar uma arte sem nome, tá certo isso?"
  DELETE_MESSAGE_CONFIRMATION_MESSAGE: ClassVar[str] = "Você tem certeza que deseja deletar a arte chamada: **`{art.name}`**?"
  DELETE_MESSAGE_NO_CONFIRMATION_MESSAGE: ClassVar[str] = "Ainda bem que tem a confirmação né não? :V"
  DELETE_MESSAGE_IF_ART_HAS_DELETED: ClassVar[str] = "A arte chamada: **`{art.name}`** foi deletada."

  @classmethod
  def _extract_art_type(cls, text: str) -> Union[ArtType, None]:
    text = fmt(text, empty='')

    if text in cls.SUPPORTED_RESPIRATION_TEXTS:
      return Art.RESPIRATION
    
    elif text in cls.SUPPORTED_KEKKIJUTSU_TEXTS:
      return Art.KEKKIJUTSU

    elif text in cls.SUPPORTED_FIGHTING_STYLE_TEXTS:
      return Art.FIGHTING_STYLE
  
  @flag(aliases=['c'])
  async def create(self, ctx: MorkatoContext, type: BaseType, names: FlagDataType) -> None:
    if type is not None:
      type = self._extract_art_type(type)
    
    cls = self.__class__
    
    if type is None:
      await ctx.send(cls.CREATE_MESSAGE_IF_TYPE_IS_NONE)
      
      return
    
    if not names:
      message: Union[str, None] = None

      if type == Art.RESPIRATION:
        message = cls.CREATE_MESSAGE_RESPIRATION_IF_NAME_IS_NONE
      
      elif type == Art.KEKKIJUTSU:
        message = cls.CREATE_MESSAGE_KEKKIJUTSU_IF_NAME_IS_NONE
      
      elif type == Art.FIGHTING_STYLE:
        message = cls.CREATE_MESSAGE_FS_IF_NAME_IS_NONE
      
      await ctx.send(message or cls.CREATE_MESSAGE_ART_IF_NAME_IS_NONE)

      return
    
    art = await ctx.morkato_guild.create_art(name=names[0], type=type)
    
    message: Union[str, None] = None

    if art.type == Art.RESPIRATION:
      message = cls.CREATE_MESSAGE_RESPIRATION_IF_HAS_CREATED
    
    if art.type == Art.KEKKIJUTSU:
      message = cls.CREATE_MESSAGE_KEKKIJUTSU_IF_HAS_CREATED
    
    if art.type == Art.FIGHTING_STYLE:
      message = cls.CREATE_MESSAGE_FS_IF_HAS_CREATED
    
    message = message or cls.CREATE_MESSAGE_ART_IF_HAS_CREATED
    
    await ctx.send(message.format(art=art))
  
  @flag(aliases=['r'])
  async def rename(self, ctx: MorkatoContext, name: BaseType, names: FlagDataType) -> None:
    cls = self.__class__

    if name is None:
      await ctx.send(cls.RENAME_MESSAGE_IF_BASE_NAME_IS_NONE)

      return
    
    if not names:
      await ctx.send(cls.RENAME_MESSAGE_IF_NAMES_HAS_NONE_NAME.format(name=name))

      return
    
    art = ctx.morkato_guild.get_art(name)

    before = art.name
    after = names[0]

    if not in_range(len(after), (2, 32)):
      await ctx.send(cls.RENAME_MESSAGE_IF_AFTER_NAME_PASS_LIMIT_RANGE)

      return

    await art.edit(name=after)

    message: Union[str, None] = None

    if art.type == Art.RESPIRATION:
      message = cls.RENAME_MESSAGE_IF_RESPIRATION_HAS_EDITED_NAME
    
    elif art.type == Art.KEKKIJUTSU:
      message = cls.RENAME_MESSAGE_IF_KEKKIJUTSU_HAS_EDITED_NAME
    
    elif art.type == Art.FIGHTING_STYLE:
      message = cls.RENAME_MESSAGE_IF_FS_HAS_EDITED_NAME
    
    message = message or cls.RENAME_MESSAGE_IF_ART_HAS_EDITED_NAME

    await ctx.send(message.format(before=before, after=after))
  
  @flag(aliases=['e'])
  async def edit(self, ctx: MorkatoContext, name: BaseType, names: FlagDataType) -> None:
    cls = self.__class__
    
    if names:
      name = names[0]
    
    if name is None:
      await ctx.send(cls.EDIT_MESSAGE_IF_NAME_IS_NONE)

      return
    
    art = ctx.morkato_guild.get_art(name)
    embed = art.embeds[0]

    origin = await ctx.send(embed=embed)

    kwargs = {  }

    while True:
      message = await ctx.bot.wait_for('message', check=message_checker(ctx, ['author', 'guild', 'channel']), timeout=300.0)

      (prefix, content) = (None, message.content)

      if ':' in content:
        (prefix, content) = content.split(':', 1)

        prefix = fmt(prefix, empty='')
      
      if prefix is None and fmt(content, empty='') in cls.EDIT_PREFIXES_DONE:
        break

      if prefix in cls.EDIT_PREFIXES_TITLE:
        if not in_range(len(content), (2, 96)):
          await message.reply(cls.EDIT_MESSAGE_IF_TITLE_PASS_LIMIT_CHARS)

          continue

        kwargs['embed_title'] = content

      elif prefix in cls.EDIT_PREFIXES_DESCRIPTION:
        if not in_range(len(content), (2, 4096)):
          await message.reply(cls.EDIT_MESSAGE_IF_DESCRIPTION_PASS_LIMIT_CHARS)

          continue

        kwargs['embed_description'] = content

      elif prefix in cls.EDIT_PREFIXES_IMAGE:
        kwargs['embed_url'] = content if not ctx.message.attachments else ctx.message.attachments[0].url
      
      embed = art.embed_at(
        title=kwargs.get('embed_title'),
        description=kwargs.get('embed_description'),
        url=kwargs.get('embed_url')
      )[0]
      
      origin = await origin.edit(embed=embed)
      await message.delete()
    
    if not kwargs:
      await ctx.send(cls.EDIT_MESSAGE_IF_KWARGS_IS_EMPTY)

      return
    
    art = await art.edit(**kwargs)

    message: Union[str, None] = None

    if art.type == Art.RESPIRATION:
      message = cls.EDIT_MESSAGE_RESPIRATION_HAS_EDITED
    
    elif art.type == Art.KEKKIJUTSU:
      message = cls.EDIT_MESSAGE_KEKKIJUTSU_HAS_EDITED
    
    elif art.type == Art.FIGHTING_STYLE:
      message = cls.EDIT_MESSAGE_FS_HAS_EDITED
    
    message = message or cls.EDIT_MESSAGE_ART_HAS_EDITED

    await ctx.send(message.format(art=art))
  
  @flag(aliases=['d'])
  async def delete(self, ctx: MorkatoContext, name: BaseType, names: FlagDataType) -> None:
    cls = self.__class__
    
    if names:
      name = names[0]
    
    if name is None:
      await ctx.send(cls.DELETE_MESSAGE_IF_NAME_IS_NONE)
      
      return
    
    art = ctx.morkato_guild.get_art(name)

    message = await ctx.send(cls.DELETE_MESSAGE_CONFIRMATION_MESSAGE.format(art=art))

    await message.add_reaction('✅')
    await message.add_reaction('❌')
    
    (reaction, user) = await ctx.bot.wait_for('reaction_add', check=reaction_checker(ctx, message, ['author', 'channel', 'message', 'guild']), timeout=30.0)
    
    if not str(reaction.emoji) == '✅':
      await ctx.send(cls.DELETE_MESSAGE_NO_CONFIRMATION_MESSAGE)
      
      return
    
    art = await art.delete()

    await ctx.send(cls.DELETE_MESSAGE_IF_ART_HAS_DELETED.format(art=art))