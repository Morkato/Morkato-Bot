-- V8: AUTOMATICALLY ATTRIBUTE INCREMENT "key" IS UNIVERSALLY.
CREATE FUNCTION convert_to_key(value name_type) RETURNS key_type AS $$
  BEGIN RETURN REGEXP_REPLACE(REGEXP_REPLACE(LOWER(unaccent(value)), '^\s+|\s+$', '', 'g'), '\s+', '-', 'g');
END; $$ LANGUAGE plpgsql;
CREATE FUNCTION autoincrement_key() RETURNS TRIGGER AS $$
BEGIN
  NEW.key := convert_to_key(NEW.name);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER "art_key"
  BEFORE INSERT OR UPDATE OF "name"
  ON "arts"
FOR EACH ROW
  EXECUTE FUNCTION autoincrement_key();

CREATE TRIGGER "attack_key"
  BEFORE INSERT OR UPDATE OF "name"
  ON "attacks"
FOR EACH ROW
  EXECUTE FUNCTION autoincrement_key();

CREATE TRIGGER "family_key"
  BEFORE INSERT OR UPDATE OF "name"
  ON "families"
FOR EACH ROW
  EXECUTE FUNCTION autoincrement_key();

CREATE TRIGGER "ability_key"
  BEFORE INSERT OR UPDATE OF "name"
  ON "abilities"
FOR EACH ROW
  EXECUTE FUNCTION autoincrement_key();