from typing import (
  Literal,

  List
)

from discord.ext   import commands

import discord

FlagChecker = Literal['author', 'guild', 'channel', 'message']

def message_checker(ctx: commands.Context, flags: List[FlagChecker]):
  def check(message: discord.Message) -> bool:
    if 'author' in flags and not message.author.id == ctx.author.id:
      return False
    
    if 'guild' in flags and not message.guild.id == ctx.guild.id:
      return False
    
    if 'channel' in flags and not message.channel.id == ctx.channel.id:
      return False
    
    return True
  return check

def reaction_checker(ctx: commands.Context, message: discord.Message, flags: List[FlagChecker]):
  def check(reaction: discord.Reaction, user: discord.User) -> bool:
    if 'author' in flags and not user.id == ctx.author.id:
      print('a')
      return False
    
    if 'guild' in flags and reaction.message.guild and not reaction.message.guild.id == ctx.guild.id:
      print('b')
      return False
    
    if 'channel' in flags and not reaction.message.channel.id == ctx.channel.id:
      print('c')
      return False
    
    if 'message' in flags and not reaction.message.id == message.id:
      print('d')
      return False
    
    return True
  
  return check
