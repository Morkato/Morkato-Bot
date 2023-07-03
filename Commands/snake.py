from discord.ext import commands

from morkato.snake import Snake, get_background
from io import BytesIO

import discord
import asyncio

members: list[int] = []

class Game(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
  
  @commands.command(name="snake-game")
  async def SnakeGame(self, ctx: commands.Context, /) -> None:
    if ctx.author.id in members:
      await ctx.send('Você já está em um jogo.')

      return
    
    members.append(ctx.author.id)
    
    snake = Snake()

    message = await ctx.send('loading...')

    await message.add_reaction('❌')
    await message.add_reaction('↪️')
    await message.add_reaction('⬅️')
    await message.add_reaction('➡️')
    await message.add_reaction('⬆️')
    await message.add_reaction('⬇️')

    async def snake_events():
      while True:
        with BytesIO() as io:
          image = get_background()

          snake.render(image)

          image.save(io, "PNG")

          io.seek(0)

          await message.edit(attachments=[discord.File(io, "frame.png")])

          snake.next()

        await asyncio.sleep(.4)

    async def reaction_manager(task):
      while True:
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=300, check=lambda reaction, user: True)
        except:
          await message.clear_reactions()

          task.cancel()

          break

        if str(reaction.emoji) == '❌':
          await message.clear_reactions()

          task.cancel()

          break

        elif str(reaction.emoji) == '↪️':
          pass

        elif str(reaction.emoji) == '⬅️' and not snake.direction == 'RIGHT':
          snake.direction = "LEFT"
        
        elif str(reaction.emoji) == '➡️' and not snake.direction == 'LEFT':
          snake.direction = "RIGHT"
        
        elif str(reaction.emoji) == '⬇️' and not snake.direction == 'UP':
          snake.direction = "DOWN"
        
        elif str(reaction.emoji) == '⬆️' and not snake.direction == 'DOWN':
          snake.direction = "UP"

        await message.remove_reaction(reaction, user)
      
      del members[members.index(ctx.author.id)]
    
    snake_task = asyncio.create_task(snake_events())
    reaction_task = asyncio.create_task(reaction_manager(snake_task))

    await asyncio.gather(
      snake_task,
      reaction_task
    )

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Game(bot))