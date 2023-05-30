-- Drop types

DROP TYPE IF EXISTS field CASCADE;

-- Drop tables

DROP TABLE IF EXISTS arts CASCADE;
DROP TABLE IF EXISTS guilds CASCADE;
DROP TABLE IF EXISTS attacks CASCADE;

-- Drop function

DROP FUNCTION IF EXISTS validate_roles CASCADE;
DROP FUNCTION IF EXISTS attack_verify_required_roles;

-- Create types

CREATE TYPE field AS (
  content text,
  roles text[],
  required_roles integer
);

-- Create functions

CREATE FUNCTION validate_roles(roles text[], re text) RETURNS boolean
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


CREATE FUNCTION attack_verify_required_roles(roles text[], required_roles integer) RETURNS boolean
AS $$
BEGIN
  RETURN array_length(roles, 1) <= required_roles;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Create tables

CREATE TABLE guilds (
  id text UNIQUE PRIMARY KEY NOT NULL,
  created_at timestamp NOT NULL DEFAULT NOW(),
  updated_at timestamp NOT NULL DEFAULT NOW(),

  CONSTRAINT check_id CHECK (id ~ '^[0-9]+$')
);

CREATE TABLE arts (
  name text NOT NULL,
  type integer NOT NULL,
  role text UNIQUE DEFAULT NULL,

  guild_id text REFERENCES guilds(id) ON DELETE CASCADE,
  
  embed_title text DEFAULT NULL,
  embed_description text DEFAULT NULL,
  embed_url text DEFAULT NULL,

  created_at timestamp NOT NULL DEFAULT NOW(),
  updated_at timestamp NOT NULL DEFAULT NOW(),

  CONSTRAINT check_name CHECK (name ~ '^[\D0-9]+$'),
  CONSTRAINT check_type CHECK (type = 0 OR type = 1 OR type = 2),
  CONSTRAINT check_role CHECK (role IS NULL OR (role ~ '^[0-9]+$')),
	
  CONSTRAINT check_embed_title CHECK (
	  embed_title IS NULL
	  OR (LENGTH(embed_title) <= 96 AND LENGTH(embed_title) > 1 AND embed_title ~ '^[\D0-9].+$')
  ),
  CONSTRAINT check_embed_description CHECK (
	  embed_description IS NULL
	  OR (LENGTH(embed_description) <= 4096 AND LENGTH(embed_description) > 1 AND embed_description ~ '^[\D0-9].+$')
  ),

  PRIMARY KEY (guild_id, name)
);

CREATE TABLE attacks (
  art_name text,
  guild_id text,

  name text NOT NULL,
  roles text[] DEFAULT '{}'::text[],
  required_roles integer DEFAULT 0,
  required_exp integer DEFAULT 0,

  damage integer DEFAULT 3000,
  stamina integer DEFAULT 3000,

  embed_title text DEFAULT NULL,
  embed_description text DEFAULT NULL,
  embed_url text DEFAULT NULL,

  fields jsonb DEFAULT '[]'::jsonb,

  CONSTRAINT check_name CHECK (name ~ '^[\D0-9]+$'),
  CONSTRAINT check_roles CHECK (validate_roles(roles, '^[0-9]+$')),
  CONSTRAINT check_required_exp CHECK (required_exp >= 0),
  CONSTRAINT check_required_roles CHECK (attack_verify_required_roles(roles, required_exp)),
  
  CONSTRAINT check_damage CHECK (damage >= 0),
  CONSTRAINT check_stamina CHECK (stamina >= 0),
  
  CONSTRAINT check_embed_title CHECK (
	  embed_title IS NULL
	  OR (LENGTH(embed_title) <= 96 AND LENGTH(embed_title) > 1 AND embed_title ~ '^[\D0-9].+$')
  ),
  CONSTRAINT check_embed_description CHECK (
	  embed_description IS NULL
	  OR (LENGTH(embed_description) <= 4096 AND LENGTH(embed_description) > 1 AND embed_description ~ '^[\D0-9].+$')
  ),
	
  CONSTRAINT fk_attacks_art FOREIGN KEY (art_name, guild_id) REFERENCES arts(name, guild_id) ON DELETE CASCADE,
  
  PRIMARY KEY (guild_id, name)
);