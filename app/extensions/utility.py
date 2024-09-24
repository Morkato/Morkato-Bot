from morkato.ext.extension import (ApplicationExtension, extension)
from morkato.ext.context import MorkatoContext
from app.checks import has_guild_permissions
from discord.interactions import Interaction
from discord import app_commands as apc
from discord.channel import TextChannel
from morkato.ext.bot import MorkatoBot
from morkato.utils import NoNullDict

guild_perms = has_guild_permissions(manage_messages=True, manage_channels=True)

@extension
class Utility(ApplicationExtension):
  @apc.command(name="ping", description="[Utilitários] Mostra meu ping atual.")
  async def ping(self, ctx: MorkatoContext) -> None:
    await ctx.send("Pong! **`%sms`**" % round(ctx.bot.latency * 1000, 2))
  @apc.command(name="wipe-category", description="[Utilitários] Wipe category from channel")
  @apc.guild_only()
  @apc.check(guild_perms)
  async def wipe_category(self, interaction: Interaction[MorkatoBot], channel: TextChannel) -> None:
    await interaction.response.defer()
    if channel.category_id == interaction.channel.category_id:
      await interaction.edit_original_response(content="Você não pode realizar está operação executando este comando nesta categoria.")
      return
    category = channel.category
    for channel in category.channels:
      kwargs = NoNullDict(
        name=channel.name,
        news=channel.is_news(),
        topic=channel.topic,
        slowmode_delay=channel.slowmode_delay,
        nsfw=channel.nsfw,
        overwrites=channel.overwrites,
        default_auto_archive_duration=channel.default_auto_archive_duration,
        default_thread_slowmode_delay=channel.default_thread_slowmode_delay
      )
      await interaction.channel.send("Recriando o canal com o nome: **`%s`** na categoria: **`%s`** mantendo as preferências." % (channel.name, category.name), reference=interaction.message)
      await category.create_text_channel(**kwargs)
      await channel.delete()
    await interaction.edit_original_response(content="Tudo certo! Os canais foram recriados.")