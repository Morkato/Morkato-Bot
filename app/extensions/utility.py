from morkato.work.project import registry
from morkato.utils import NoNullDict
from app.checks import has_guild_permissions
from app.extension import BaseExtension
from discord.interactions import Interaction
from discord.channel import TextChannel
from discord import app_commands as apc
import app.errors

guild_perms = has_guild_permissions(manage_messages=True, manage_channels=True)

@registry
class Utility(BaseExtension):
  LANGUAGE = "ptBR"
  @apc.command(
    name="ping",
    description="[Utilitários] Mostra meu ping atual."
  )
  async def ping(self, interaction: Interaction) -> None:
    await interaction.response.defer()
    content = self.builder.get_content(self.LANGUAGE, "onPing", round(interaction.client.latency * 1000, 2))
    await interaction.edit_original_response(content=content)
  @apc.command(name="wipe-category", description="[Utilitários] Wipe category from channel")
  @apc.guild_only()
  @apc.check(guild_perms)
  async def wipe_category(self, interaction: Interaction, channel: TextChannel) -> None:
    await interaction.response.defer()
    if channel.category_id == interaction.channel.category_id:
      content = self.get_content(self.LANGUAGE, "itsSelfOnWipeCategory")
      await interaction.edit_original_response(content=content)
      return
    category = channel.category
    is_creating_content = self.builder.get_content_unknown_formatting(self.LANGUAGE, "channelCreatingOnWipeCategory")
    is_created_channel = self.builder.get_content_unknown_formatting(self.LANGUAGE, "channelCreatedMessage")
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
      await interaction.edit_original_response(content=is_creating_content.format(channel=channel, category=category))
      new_channel = await category.create_text_channel(**kwargs)
      await channel.delete()
      await new_channel.send(is_created_channel.format(author=interaction.user))
    content = self.get_content(self.LANGUAGE, "wipeDone")
    await interaction.edit_original_response(content=content)
  @apc.command(
    name = "cache-clean",
    description = "[Utilitário] Limpa o meu cache."
  )
  async def cache_clean(self, interaction: Interaction) -> None:
    content = self.builder.get_content(self.LANGUAGE, "cacheCleanConfirmation")
    conf = await self.send_confirmation(interaction, content = content)
    if not conf:
      raise app.errors.NoActionError
    self.connection.clear()
    content = self.builder.get_content(self.LANGUAGE, "cacheCleanContentMessage")
    await interaction.edit_original_response(content=content, view=None)