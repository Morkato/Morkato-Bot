CREATE FUNCTION sync_npc_energy_with_ability() RETURNS TRIGGER AS $$
DECLARE
  ability abilities%ROWTYPE;
  updated INTEGER;
BEGIN
  SELECT *
    INTO ability
    FROM abilities ab
  WHERE ab.guild_id = NEW.guild_id
    AND ab.id = NEW.ability_id
  LIMIT 1;
  IF NOT FOUND THEN
    RAISE EXCEPTION 'No ability found for guild_id % and ability_id %', NEW.guild_id, NEW.ability_id;
  END IF;
  UPDATE "npcs" SET
    max_energy = max_energy + ability.energy,
    energy = max_energy + ability.energy
  WHERE guild_id = NEW.guild_id
    AND id = NEW.npc_id;
  GET DIAGNOSTICS updated = ROW_COUNT;
  IF updated <> 1 THEN
    RAISE EXCEPTION 'Updated <> 1 npcs, where: guild_id % npc_id %', NEW.guild_id, NEW.npc_id;
  END IF;
  RETURN NEW;
END; $$ LANGUAGE plpgsql;
CREATE FUNCTION sync_npc_with_player() RETURNS TRIGGER AS $$
DECLARE
  _player_id discord_id_type;
  ability_ids id_type[];
  ability_id id_type;
  max_energy energy_type;
BEGIN
  IF NEW.player_id IS NULL THEN
    RETURN NEW;
  END IF;
  _player_id := NEW.player_id;
    SELECT
      array_agg(ability.id),
      SUM(ability.energy)
    INTO ability_ids, max_energy
    FROM "players_abilities" pa
    INNER JOIN "abilities" ability
      ON ability.guild_id = pa.guild_id
        AND ability.id = pa.ability_id
    WHERE pa.guild_id = NEW.guild_id
      AND pa.player_id = _player_id;
  FOREACH ability_id IN ARRAY ability_ids LOOP
    INSERT INTO "npcs_abilities"("guild_id","npc_id","ability_id")
      VALUES (NEW.guild_id,NEW.id,ability_id);
  END LOOP;
  NEW.max_energy := NEW.max_energy + max_energy;
  NEW.energy := NEW.max_energy;
  RETURN NEW;
END; $$ LANGUAGE plpgsql;
CREATE TRIGGER "sync_npc_with_player"
  AFTER INSERT
  ON "npcs"
FOR EACH ROW
  EXECUTE FUNCTION sync_npc_with_player();
CREATE TRIGGER "sync_npc_energy_with_ability"
  BEFORE INSERT
  ON "npcs_abilities"
FOR EACH ROW
  EXECUTE FUNCTION sync_npc_energy_with_ability();