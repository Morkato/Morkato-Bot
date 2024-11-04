from discord.ext import commands
from discord import (Interaction, Permissions)
from typing import Union

def has_guild_permissions(**perms):
  invalid = set(perms) - set(Permissions.VALID_FLAGS)
  if invalid:
    raise TypeError(f"Invalid permission(s): {', '.join(invalid)}")
  def predicate(ctx: Union[Interaction, commands.Context]) -> bool:
    if ctx.guild == None:
      raise commands.NoPrivateMessage
    user = ctx.author if isinstance(ctx, commands.Context) else ctx.user
    permissions = user.guild_permissions # type: ignore
    missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]
    return not missing
  return predicate