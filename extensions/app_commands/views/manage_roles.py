from typing import List

from discord import (
  Interaction,
  Role,

  app_commands,
  ui
)

colors = [
  app_commands.Choice(name="Preto", value=0),
  app_commands.Choice(name="Preto Claro", value=42875),
  app_commands.Choice(name="Ciano", value=1752220),
  app_commands.Choice(name="Ciano Escuro", value=1146986),
  app_commands.Choice(name="Verde", value=5763719),
  app_commands.Choice(name="Verde Escuro", value=2067276),
  app_commands.Choice(name="Azul", value=3447003),
  app_commands.Choice(name="Azul Escuro", value=2123412),
  app_commands.Choice(name="Roxo", value=10181046),
  app_commands.Choice(name="Roxo Escuro", value=7419530),
  app_commands.Choice(name="Rosa Vivo Luminoso", value=15277667),
  app_commands.Choice(name="Rosa Vivo Escuro", value=11342935),
  app_commands.Choice(name="Amarelo Ouro", value=15844367),
  app_commands.Choice(name="Amarelo Ouro Escuro", value=12745742),
  app_commands.Choice(name="Laranja", value=15105570),
  app_commands.Choice(name="Laranja Escuro", value= 	11027200),
  app_commands.Choice(name="Vermelho", value=15548997),
  app_commands.Choice(name="Vermelho Escuro", value=10038562),
  app_commands.Choice(name="Cinza", value=9807270),
  app_commands.Choice(name="Cinza Escuro", value=9936031),
  app_commands.Choice(name="Cinza Preto", value=8359053),
  app_commands.Choice(name="Cinza Claro", value=12370112),
  app_commands.Choice(name="Navvy", value=3426654),
  app_commands.Choice(name="Navvy Escuro", value=2899536),
  app_commands.Choice(name="Amarelo", value=16776960)
]

class MoveRoleView(ui.View):
  TIMEOUT = 20
  
  def __init__(self, roles: List[Role], to: Role):
    super().__init__(timeout=MoveRoleView.TIMEOUT)

    self.roles  = roles
    self.to     = to

    self.closed = False

  async def on_timeout(self) -> None: ...

  @ui.button(
    label="✅",
    custom_id="yeh"
  )
  async def accept(self, interaction: Interaction, button: ui.Button) -> None:
    if self.closed: return

    await interaction.response.defer()

    self.closed = True
    
    async with interaction.channel.typing():

      pos = self.to.position
    
      for role in self.roles:
        role = await role.edit(position=pos if not pos < 1 else 1)

        pos = role.position
    
      await interaction.edit_original_response(content="Tudo certo, movi para o local que você queria.", view=None)

  @ui.button(
    label='❌',
    custom_id="nop"
  )
  async def notAccept(self, interaction: Interaction, button: ui.Button) -> None:
    if self.closed: return

    self.closed = True

    await interaction.response.edit_message(content="Ainda bem que tem a confirmação né não?", view=None)

    

