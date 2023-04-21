# Objetivo do Projeto
  O objetivo do projeto é ser um RPG/RP de Kimetsu no Yaiba no discord: Usando Python para o Bot; Nodejs para Back-end e Front-end; PostgreSQL para Banco de dados.
  
  Predendo recriar quase todos os sistemas presentes no Anime, como: 
  1.  Respirações e Kekkijutsus, que iremos chamar de "Arts" para simplificar. Não poderá existir Arts com mesmo nome, mesmo sendo de tipos diferentes. Cada Art também tendo os ataques que iremos chamar de "Formas" assim como no anime. As Formas será global para todos, ou seja, não poerá ter Formas com o mesmo nome mesmo em Arts deferentes;
  2.  Um sistema de NPC podendo ser controlado por um ADM e ter as mesmas coisas que um player comum tem;
  3.  Um sistema de items, com esse tendo cormécio ou leilão entre jogadores ou NPCS, tendo também um sistema de raridade, podendo ser achado em possíveis canais, sendo opicional: um sistema de durabilidade e quantidade;
  4.  Uma loja para cada chat, sendo possível achar items em certos canais;
  5.  Por fim, um sistema de players, podendo ter `exp`, `inventário` e um `dashboard` tando no discord quanto no front-end.

# Funcionalidades para o Bot
  O bot como mencionado, será implementado no Python, tendo comandos para loja, NPC, Arts e players, mas também, terá um Regex onde só é capturado em certos canais possíveis "Formas" de cada Art para certos players.

# Back-end (Foco)
  1.  O Back-end funcionará para usuários do discord, ou seja, tendo um "Bearer Token" valido com acesso ao Servidores do usuário;
  2.  API pública para acesso ao Banco de Dados, tendo como header obrigatório o "Bearer Token" valido **`(/api/v1)`**;
  3.  Uma API privada para o Bot, tendo um secret-token que somente os desenvolvedores sabem para acesso ao Banco de Dados **`(/api/bot/v1)`**.