from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
  from discord.interactions import Interaction
  from discord.ui.button import Button
  from discord.role import Role

from discord.app_commands.models import Choice
from discord.ui.button import button
from discord.ui.view import View

colors = [
  Choice(name="Preto", value=0),
  Choice(name="Preto Claro", value=42875),
  Choice(name="Ciano", value=1752220),
  Choice(name="Ciano Escuro", value=1146986),
  Choice(name="Verde", value=5763719),
  Choice(name="Verde Escuro", value=2067276),
  Choice(name="Azul", value=3447003),
  Choice(name="Azul Escuro", value=2123412),
  Choice(name="Roxo", value=10181046),
  Choice(name="Roxo Escuro", value=7419530),
  Choice(name="Rosa Vivo Luminoso", value=15277667),
  Choice(name="Rosa Vivo Escuro", value=11342935),
  Choice(name="Amarelo Ouro", value=15844367),
  Choice(name="Amarelo Ouro Escuro", value=12745742),
  Choice(name="Laranja", value=15105570),
  Choice(name="Laranja Escuro", value= 	11027200),
  Choice(name="Vermelho", value=15548997),
  Choice(name="Vermelho Escuro", value=10038562),
  Choice(name="Cinza", value=9807270),
  Choice(name="Cinza Escuro", value=9936031),
  Choice(name="Cinza Preto", value=8359053),
  Choice(name="Cinza Claro", value=12370112),
  Choice(name="Navvy", value=3426654),
  Choice(name="Navvy Escuro", value=2899536),
  Choice(name="Amarelo", value=16776960)
]

class MoveRoleView(View):
  TIMEOUT = 20
  
  def __init__(self, roles: List[Role], to: Role):
    super().__init__(timeout=MoveRoleView.TIMEOUT)

    self.roles  = roles
    self.to     = to

    self.closed = False

  async def on_timeout(self) -> None: ...

  @button(
    label="✅",
    custom_id="yeh"
  )
  async def accept(self, interaction: Interaction, button: Button) -> None:
    if self.closed: return

    await interaction.response.defer()

    self.closed = True
    
    async with interaction.channel.typing():

      pos = self.to.position
    
      for role in self.roles:
        role = await role.edit(position=pos if not pos < 1 else 1)

        pos = role.position
    
      await interaction.edit_original_response(content="Tudo certo, movi para o local que você queria.", view=None)

  @button(
    label='❌',
    custom_id="nop"
  )
  async def notAccept(self, interaction: Interaction, button: Button) -> None:
    if self.closed: return

    self.closed = True

    await interaction.response.edit_message(content="Ainda bem que tem a confirmação né não?", view=None)

class ConfirmationDeleteRole(View):
  TIMEOUT = 20

  def __init__(self, role: Role) -> None:
    super().__init__(timeout=ConfirmationDeleteRole.TIMEOUT)

    self.closed = False
    self.role = role
  
  @button(
    label="✅",
    custom_id="yeh"
  )
  async def accept(self, interaction: Interaction, button: Button) -> None:
    if self.closed: return

    await interaction.response.defer()

    self.closed = True
    
    await self.role.delete()

    await interaction.edit_original_response(content=f"Tudo certo, deletei o cargo chamado: **`@{self.role.name}`**", view=None)
  
  @button(
    label='❌',
    custom_id="nop"
  )
  async def notAccept(self, interaction: Interaction, button: Button) -> None:
    if self.closed: return

    self.closed = True

    await interaction.response.edit_message(content="Ainda bem que tem a confirmação né não?", view=None)