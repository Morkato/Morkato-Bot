from discord.ext import commands
import discord

async def message_page_embeds(ctx: commands.Context, bot: commands.Bot, embeds: list[discord.Embed]) -> None:
  message = await ctx.send(embed=embeds[0])

  length = len(embeds)

  if length == 1:
    return
  
  index = 0

  await message.add_reaction('⏪')
  await message.add_reaction('⏩')

  while True:
    try:
      reaction, user = await bot.wait_for('reaction_add', timeout=20, check= lambda reaction, user: user.id == ctx.author.id and ctx.guild.id == reaction.message.guild.id and ctx.channel.id == reaction.message.channel.id and message.id == reaction.message.id)
    except:
      await message.clear_reactions()

      return
    
    if str(reaction.emoji) == '⏪':
      index = length - 1 if index == 0 else index - 1

      await message.remove_reaction('⏪', user)
    elif str(reaction.emoji) == '⏩':
      index = 0 if index + 1 == length else index + 1

      await message.remove_reaction('⏩', user)

    await message.edit(embed=embeds[index])