CREATE function array_is_valid(roles text[], re text) RETURNS boolean
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

CREATE FUNCTION check_required_roles(required_roles int, roles text[])  RETURNS boolean
AS $$
BEGIN
  RETURN CASE WHEN required_roles > 0 AND required_roles <= array_length(roles, 1) THEN TRUE ELSE FALSE END;
END;
$$ LANGUAGE plpgsql IMMUTABLE;


ALTER TABLE guilds ADD CONSTRAINT check_id CHECK (id ~ '^[0-9]+$');

ALTER TABLE arts ADD CONSTRAINT check_name CHECK (LENGTH(name) > 1 AND LENGTH(name) < 32 AND name ~ '^[^\d \n\t\v\r\f\b]+$');
ALTER TABLE arts ADD CONSTRAINT check_embed_title CHECK (embed_title IS NULL OR LENGTH(embed_title) > 0 AND LENGTH(embed_title) <= 96);
ALTER TABLE arts ADD CONSTRAINT check_embed_description CHECK (embed_description IS NULL OR LENGTH(embed_description) > 0 AND LENGTH(embed_description) < 4096);
ALTER TABLE arts ADD CONSTRAINT check_url CHECK (embed_url IS NULL OR embed_url ~ '^(https?://|cdn:/)[^\d \n\t\v\r\f\b]+$');
ALTER TABLE arts ADD CONSTRAINT check_role CHECK (role IS NULL OR (role ~ '^[0-9]+$'));

ALTER TABLE attacks ADD CONSTRAINT check_name CHECK (LENGTH(name) > 1 AND LENGTH(name) < 32 AND name ~ '^[^\d \n\t\v\r\f\b]+$');
ALTER TABLE attacks ADD CONSTRAINT check_roles CHECK (array_is_valid(roles, '^0-9$'));
ALTER TABLE attacks ADD CONSTRAINT check_required_exp CHECK (check_required_roles(required_roles, roles));
ALTER TABLE attacks ADD CONSTRAINT check_damage CHECK (damage >= 0);
ALTER TABLE attacks ADD CONSTRAINT check_stamina CHECK (stamina >= 0);
ALTER TABLE attacks ADD CONSTRAINT check_embed_title CHECK (embed_title IS NULL OR LENGTH(embed_title) > 0 AND LENGTH(embed_title) <= 96);
ALTER TABLE attacks ADD CONSTRAINT check_embed_description CHECK (embed_description IS NULL OR LENGTH(embed_description) > 0 AND LENGTH(embed_description) < 4096);
ALTER TABLE attacks ADD CONSTRAINT check_url CHECK (embed_url IS NULL OR embed_url ~ '^(https?://|cdn:/)[^\d \n\t\v\r\f\b]+$');

ALTER TABLE attacks_fields ADD CONSTRAINT check_text CHECK (LENGTH(text) > 0 AND LENGTH(text) <= 132 );
ALTER TABLE attacks_fields ADD CONSTRAINT check_required_exp CHECK (array_is_valid(roles, '^[0-9]+$'));