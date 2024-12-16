from morkbmt.extension import ExtensionCommandBuilder
from morkbmt.core import registry
from morkato.utils import NoNullDict
from app.extension import BaseExtension
from discord.interactions import Interaction
from discord.message import Attachment
from discord.channel import TextChannel
from discord import app_commands as apc
from typing_extensions import Self
from typing import (
  Optional,
  ClassVar
)
import discord.ext.commands
import app.errors
import aiohttp
import os

@registry
class Utility(BaseExtension):
  GUILD_ID: ClassVar[Optional[int]] = None
  async def setup(self, commands: ExtensionCommandBuilder[Self]) -> None:
    self.LANGUAGE = self.msgbuilder.PT_BR
    self.has_guild_perms = discord.ext.commands.has_guild_permissions(manage_messages=True, manage_channels=True)
    self.is_owner_guild = lambda ctx: self.GUILD_ID is not None and ctx.guild.id == self.GUILD_ID
    image_upload = commands.app_command("image-upload", self.image_upload_from_attach, description="[Utilitários] Upa uma imagem para minha cdn.")
    image_upload_url = commands.app_command("image-upload-url", self.image_upload_from_url, description="[Utilitários] Upa uma imagem para minha cdn.")
    wipe_category = commands.app_command("wipe-category", self.wipe_category, description="[Utilitários] Wipe category from channel.")
    cache_clean = commands.app_command("cache-clean", self.cache_clean, description = "[Utilitário] Limpa o meu cache.")
    commands.app_command("ping", self.ping, description="[Utilitários] Mostra meu ping atual.")
    
    commands.check(image_upload, self.has_guild_perms)
    commands.check(image_upload, self.is_owner_guild)
    commands.check(image_upload_url, self.has_guild_perms)
    commands.check(image_upload_url, self.is_owner_guild)
    commands.check(cache_clean, self.has_guild_perms)
    commands.check(cache_clean, self.is_owner_guild)
    commands.check(wipe_category, self.has_guild_perms)

    commands.guild_only(image_upload)
    commands.guild_only(image_upload_url)
    commands.guild_only(cache_clean)
    commands.guild_only(wipe_category)
  async def image_upload(self, interaction: Interaction, filename: str, image: bytes) -> None:
    await self.connection.upload_image(
      author_id=interaction.user.id,
      name=filename,
      image=image
    )
    content = self.builder.safe_get_content(self.LANGUAGE, "uploadImage", author_id=interaction.user.id, name=filename)
    await interaction.edit_original_response(content=content)
  async def image_upload_from_attach(self, interaction: Interaction, filename: str, attachment: Attachment) -> None:
    await interaction.response.defer()
    attach_data = await attachment.read()
    await self.image_upload(interaction, filename, attach_data)
  async def image_upload_from_url(self, interaction: Interaction, filename: str, url: str) -> None:
    await interaction.response.defer()
    image: bytes
    async with aiohttp.ClientSession() as session:
      async with session.request("GET", url) as resp:
        image = await resp.content.read()
    await self.image_upload(interaction, filename, image)
  async def ping(self, interaction: Interaction) -> None:
    await interaction.response.defer()
    content = self.builder.get_content(self.LANGUAGE, "onPing", round(interaction.client.latency * 1000, 2))
    await interaction.edit_original_response(content=content)
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
  async def cache_clean(self, interaction: Interaction) -> None:
    content = self.builder.get_content(self.LANGUAGE, "cacheCleanConfirmation")
    conf = await self.send_confirmation(interaction, content = content)
    if not conf:
      raise app.errors.NoActionError
    self.connection.clear()
    content = self.builder.get_content(self.LANGUAGE, "cacheCleanContentMessage")
    await interaction.edit_original_response(content=content, view=None)
guild_id = os.getenv("GUILD_ID")
if guild_id is not None:
  Utility.GUILD_ID = int(guild_id)