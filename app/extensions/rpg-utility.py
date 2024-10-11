from morkato.types import (AbilityType, NpcType, ArtType)
from morkato.errors import (NotFoundError, MorkatoHTTPType)
from morkato.work.builder import MessageBuilder
from morkato.work.project import registry
from morkato.attack import AttackIntents
from discord.interactions import Interaction
from discord import app_commands as apc
from discord.user import User
from app.extension import BaseExtension
from typing import (
  Optional,
  ClassVar,
  Dict
)
import app.checks
import app.utils

has_guild_perms = app.checks.has_guild_permissions(manage_guild=True)

@registry
class RPGUtility(BaseExtension):
  LANGUAGE: ClassVar[str] = MessageBuilder.PT_BR
  ART_CREATED: ClassVar[str] = "Uma nova arte com o nome: **`{art.name}`** foi criada!"
  ATTACK_INTENTS_CHOICES = [
    apc.Choice(name="Indesviável", value=AttackIntents.UNAVOIDABLE),
    apc.Choice(name="Indefensável", value=AttackIntents.INDEFENSIBLE),
    apc.Choice(name="Em área", value=AttackIntents.AREA),
    apc.Choice(name="Não contra atacável", value=AttackIntents.NOT_COUNTER_ATTACKABLE),
    apc.Choice(name="Contra ataque", value=AttackIntents.COUNTER_ATTACKABLE),
    apc.Choice(name="Usável para defesa", value=AttackIntents.DEFENSIVE)
  ]
  ATTACK_INTENTS_MESSAGE_MAP: ClassVar[Dict[int, str]] = {
    AttackIntents.UNAVOIDABLE: "As intenções de ataque foram alteradas. Agora esse ataque é indesviável (Attack Intents: **`{intents}`**)",
    AttackIntents.INDEFENSIBLE: "As intenções de ataque foram alteradas. Agora esse ataque é indefensável (Attack Intents: **`{intents}`**)",
    AttackIntents.AREA: "As intenções de ataque foram alteradas. Agora esse ataque é em área (Attack Intents: **`{intents}`**)",
    AttackIntents.NOT_COUNTER_ATTACKABLE: "As intenções de ataque foram alteradas. Agora esse ataque não é contra atacável (Attack Intents: **`{intents}`**)",
    AttackIntents.COUNTER_ATTACKABLE: "As intenções de ataque foram alteradas. Agora esse ataque pode ser usado para contra ataque (Attack Intents: **`{intents}`**)",
    AttackIntents.DEFENSIVE: "As intenções de ataque foram alteradas. Agora esse ataque pode ser usado para defesa (Attack Intents: **`{intents}`**)"
  }
  @apc.command(
    name="art-create",
    description="[RPG Utilitários] Cria uma nova arte."
  )
  @apc.guild_only()
  @apc.check(has_guild_perms)
  async def art_create(self, interaction: Interaction, name: str, type: ArtType, description: Optional[str], banner: Optional[str]) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    art = await guild.create_art(
      name=name,
      type=type,
      description=description,
      banner=banner
    )
    content = self.builder.get_content(self.LANGUAGE, "onArtCreate", art.name)
    await interaction.edit_original_response(content=content)
  @apc.command(
    name="art-update",
    description="[RPG Utilitários] atualiza uma arte existente."
  )
  @apc.rename(art_query="art")
  @apc.guild_only()
  @apc.check(has_guild_perms)
  async def art_update(
    self,
    interaction: Interaction, art_query: str,
    name: Optional[str], type: Optional[ArtType],
    desc: Optional[str], banner: Optional[str]
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    art = await app.utils.ArtConverter()._get_art_by_guild(guild, art_query)
    await art.edit(
      name = name,
      type = type,
      description = desc,
      banner = banner
    )
    
    await interaction.edit_original_response(content="A arte chamada: **`%s`** foi atualizada!" % art.name)
  @apc.command(
    name="attack-create",
    description="[RPG Utilitários] Cria um novo ataque."
  )
  @apc.rename(art_query="art")
  @apc.guild_only()
  @apc.check(has_guild_perms)
  async def attack_create(
    self,
    interaction: Interaction, art_query: str,
    name: str, prefix: Optional[str],
    resumed_description: Optional[str], description: Optional[str],
    banner: Optional[str], damage: Optional[int],
    breath: Optional[int], blood: Optional[int]
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    if not guild.arts.already_loaded():
      await guild.arts.resolve()
    art = await app.utils.ArtConverter()._get_art_by_guild(guild, art_query)
    attack = app.utils.AttackConverter()._get_next_attack_by_name(guild, name)
    if attack is not None:
      if attack.art.id == art.id:
        raise NotImplementedError
      confirmation = await self.send_confirmation(interaction, content="Existe outro ataque com o mesmo nome na arte: **`%s`**. Caso crie nesta arte, você terá que especificar a arte no ataque. Tem certeza?" % attack.art.name)
      if not confirmation:
        await interaction.edit_original_response(content="Como é bom ter uma confirmação né?")
        return
    attack = await art.create_attack(
      name=name,
      name_prefix_art=prefix,
      description=description,
      resume_description=resumed_description,
      banner=banner,
      damage=damage,
      breath=breath,
      blood=blood
    )
    await interaction.edit_original_response(content="Um novo ataque chamado: **`%s`** para a arte: **`%s`** foi criado!" % (attack.name, art.name))
  @apc.command(
    name="attack-set-intent",
    description="[RPG Utilitários] Manipula as intenções de um ataque."
  )
  @apc.guild_only()
  @apc.choices(intent=ATTACK_INTENTS_CHOICES)
  @apc.rename(attack_query="attack")
  @apc.guild_only()
  @apc.check(has_guild_perms)
  async def attack_set_intent(self, interaction: Interaction, attack_query: str, intent: int) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    if not guild.arts.already_loaded():
      await guild.arts.resolve()
    attack = await app.utils.AttackConverter()._get_attack_by_guild(guild, attack_query)
    if attack.intents.has_intent(intent):
      await interaction.edit_original_response(content="Esse ataque já tem essa intenção.")
      return
    intents = AttackIntents(attack.intents)
    intents.set(intent)
    await attack.edit(intents=intents)
    content = self.ATTACK_INTENTS_MESSAGE_MAP[intent].format(intents=intents)
    await interaction.edit_original_response(content=content)
  @apc.command(
    name="attack-reset-intents",
    description="[RPG Utilitários] Volta as intenções de uma ataque para padrão."
  )
  @apc.rename(attack_query="attack")
  @apc.guild_only()
  @apc.check(has_guild_perms)
  async def attack_reset_intents(self, interaction: Interaction, attack_query: str) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    if not guild.arts.already_loaded():
      await guild.arts.resolve()
    attack = await app.utils.AttackConverter()._get_attack_by_guild(guild, attack_query)
    if attack.intents.is_empty():
      await interaction.edit_original_response(content="Esse ataque já não possui intenções (Attack Intents: **`%s`**)" % attack.intents)
      return
    intents = attack.intents
    await attack.edit(intents=AttackIntents())
    await interaction.edit_original_response(content="As intenções do ataque foram restauradas de **`%s`** para **`%s`**" % (intents, attack.intents))
  @apc.command(
    name="attack-update",
    description="[RPG Utilitários] Atualiza o ataque desejado."
  )
  @apc.rename(attack_query="attack")
  @apc.guild_only()
  @apc.check(has_guild_perms)
  async def attack_update(
    self, 
    interaction: Interaction, attack_query: str,
    name: Optional[str], prefix: Optional[str],
    resumed_description: Optional[str], description: Optional[str],
    banner: Optional[str], damage: Optional[int],
    breath: Optional[int], blood: Optional[int]
  ) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    if not guild.arts.already_loaded():
      await guild.arts.resolve()
    attack = await app.utils.AttackConverter()._get_attack_by_guild(guild, attack_query)
    last_name = attack.name
    attack = await attack.edit(
      name=name,
      name_prefix_art=prefix,
      description=description,
      resume_description=resumed_description,
      banner=banner,
      damage=damage,
      breath=breath,
      blood=blood
    )
    await interaction.edit_original_response(content="O ataque chamado: **`%s`** foi atualizado." % last_name)
  @apc.command(
    name="npc-create",
    description="[RPG Utilitários] Cria um novo npc."
  )
  @apc.guild_only()
  @apc.check(has_guild_perms)
  async def npc_create(self, interaction: Interaction, name: str, surname: str, type: NpcType) -> None:
    await interaction.response.defer()
    if surname.lower() in ["self", "this"]:
      await interaction.edit_original_response(content="Você não pode colocar o apelido: **`%s`** pois esta, é uma palavra reservada." % surname)
      return
    guild = await self.get_morkato_guild(interaction.guild)
    npc = await guild.create_npc(name=name, surname=surname, type=type)
    content = "Um novo npc chamado: **`%s`** foi criado (Apelido: %s)." % (npc.name, npc.surname)
    await interaction.edit_original_response(content=content + "\n**OBS:** É impossível um jogador conseguir controlar este npc, por isso as variáveis **`self`** e **`this`** estarão indisponíveis.")
  @apc.command(
    name="set-player-type",
    description="[RPG Utilitários] Monta o contexto para um jogador"
  )
  @apc.guild_only()
  async def create_player(self, interaction: Interaction, type: NpcType) -> None:
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    player = await guild.create_player(interaction.user, type)
    content = "Seu contexto agora é **`%s`** (Quando o contexto é definido, é impossível editá-lo. Apague-o caso se arrependa).\n**`%s`**" % (type, player)
    await interaction.edit_original_response(content=content)
  
  @apc.command(
    name="preset",
    description="[RPG Utilitários] Excluí o contexto para um jogador"
  )
  @apc.guild_only()
  async def player_reset(self, interaction: Interaction, user: User) -> None:
    if not interaction.user.guild_permissions.manage_guild:
      await interaction.response.send_message("Você não tem permissão suficiente para executar esta ação.")
      return
    await interaction.response.defer()
    guild = await self.get_morkato_guild(interaction.guild)
    player = guild.get_cached_player(user.id)
    if player is None:
      try:
        player = await guild.fetch_player(user.id)
      except NotFoundError as exc:
        if exc.type != MorkatoHTTPType.PLAYER_NOTFOUND:
          raise exc
        await interaction.edit_original_response(content="Este jogador ainda não possuí contexto, o que você quer excluir?")
        return
    await player.delete()
    await interaction.edit_original_response(content="Foi excluído o contexto do jogador: **`%s`**" % (user.name))
  @apc.command(
    name="pregister",
    description="[RPG Utilitários] Registra um jogador"
  )
  @apc.guild_only()
  async def player_register(
    self, interaction: Interaction, *,
    user: User,
    name: str,
    surname: str
  ) -> None:
    guild = await self.get_morkato_guild(interaction.guild)
    player = guild.get_cached_player(interaction.user.id)
    if player is None:
      player = await guild.fetch_player(interaction.user.id)
    if player.already_registered():
      content = self.builder.get_content(self.LANGUAGE, "onPlayerAlreadyRegistered")
      await interaction.response.send_message(content)
      return
    await interaction.response.defer()
    npc = await player.registry(name, surname)
    await interaction.edit_original_response(content=repr(npc))