from typing import Optional

from easy_pil       import load_image_async
from discord.ext    import commands
from io             import BytesIO
from objects.player import Player
from morkato.client import MorkatoBot

from discord.errors import NotFound

import discord

async def regenere_webhook(ctx: commands.Context, player: Player) -> discord.Webhook:
  url = player.appearance or ctx.author.display_avatar.url

  image = await load_image_async(url)

  image_bytes = None
  
  with BytesIO() as buffer:
    image.save(buffer, 'PNG')

    buffer.seek(0)

    image_bytes = buffer.read()

  webhook = await ctx.channel.create_webhook(name=player.name, avatar=image_bytes)

  await player.edit(webhook=webhook)

  return webhook

async def create_webhook(channel: discord.TextChannel, member: discord.Member, player: Player) -> discord.Webhook:
  avatar = player.appearance or member.display_avatar.url
  
  image = await load_image_async(avatar)

  if not image:
    return await channel.create_webhook(name=player.name)
  
  image_bytes = None
  
  with BytesIO() as buffer:
    image.save(buffer, 'PNG')

    buffer.seek(0)

    image_bytes = buffer.read()
  
  webhook = await channel.create_webhook(name=player.name, avatar=image_bytes)

  return webhook

async def extract_webhook(ctx: commands.Context, client: MorkatoBot, player: Player, member: Optional[discord.Member] = None) -> discord.Webhook:
  if not member:
    member = ctx.author
  
  webhook = await create_webhook(ctx.channel, member, player)

  return webhook


