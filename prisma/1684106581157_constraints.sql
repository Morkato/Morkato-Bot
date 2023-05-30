CREATE OR REPLACE function array_is_valid(roles text[], re text) RETURNS boolean
AS $$
DECLARE
  roles_len int := array_length(roles, 1);
  i int := 1;
BEGIN
  IF roles_len = 0 THEN
    RETURN TRUE;
  END IF;

  WHILE i <= roles_len LOOP
    IF NOT (roles[i] ~ re) THEN
      RETURN FALSE;
    END IF;
  END LOOP;
  
  RETURN TRUE;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION check_required_roles(required_roles int, roles text[])  RETURNS boolean
AS $$
BEGIN
  IF (array_length(roles, 1) is NULL) THEN
    RETURN TRUE;
  END IF;
  RETURN CASE WHEN required_roles > 0 AND required_roles <= array_length(roles, 1) THEN TRUE ELSE FALSE END;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION check_text(text TEXT, min Int, max Int, re text = null)
RETURNS boolean AS $$
DECLARE
  re_formate text := CASE WHEN re is null THEN '.+' ELSE re END;
BEGIN
  RETURN CASE WHEN LENGTH(text) > min AND LENGTH(text) <= max AND text ~ re_formate THEN TRUE ELSE FALSE END;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION check_embed(title text, description text, url text) RETURNS boolean
AS $$
DECLARE
  title_check boolean       := title is null OR check_text(title, 0, 90);
  description_check boolean := description is null OR check_text(description, 0, 4096);
  url_check boolean         := url is null OR url ~ '^(https?://|cdn:/)[^\d \n\t\v\r\f\b]+$';
BEGIN
  RETURN CASE WHEN title_check AND description_check AND url_check THEN TRUE ELSE FALSE END;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

ALTER TABLE guilds ADD CONSTRAINT check_id CHECK (id ~ '^[0-9]+$');

ALTER TABLE arts ADD CONSTRAINT check_name CHECK (check_text(name, 1, 32, '^[\D0-9]+$'));
ALTER TABLE arts ADD CONSTRAINT check_art_name_is_type CHECK (NOT name ~ 'RESPIRATION|KEKKIJUTSU|ATTACK');
ALTER TABLE arts ADD CONSTRAINT check_embed CHECK (check_embed(embed_title, embed_description, embed_url));
ALTER TABLE arts ADD CONSTRAINT check_role CHECK (role IS NULL OR (role ~ '^[0-9]+$'));

ALTER TABLE attacks ADD CONSTRAINT check_name CHECK (check_text(name, 1, 32, '^[\D0-9]+$'));
ALTER TABLE attacks ADD CONSTRAINT check_roles CHECK (array_is_valid(roles, '^[0-9]+$'));
ALTER TABLE attacks ADD CONSTRAINT check_required_roles CHECK (check_required_roles(required_roles, roles));
ALTER TABLE attacks ADD CONSTRAINT check_damage CHECK (damage >= 0);
ALTER TABLE attacks ADD CONSTRAINT check_stamina CHECK (stamina >= 0);
ALTER TABLE attacks ADD CONSTRAINT check_embed CHECK (check_embed(embed_title, embed_description, embed_url));

ALTER TABLE attacks_fields ADD CONSTRAINT check_text CHECK (check_text(text, 1, 132));
ALTER TABLE attacks_fields ADD CONSTRAINT check_required_exp CHECK (array_is_valid(roles, '^[0-9]+$'));