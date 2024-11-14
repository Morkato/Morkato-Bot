-- V1 CREATE FUNCTION WITH SNOWFLAKE ALGORITHM
CREATE SEQUENCE global_snowflake_seq;
CREATE FUNCTION snowflake_id(seq_name TEXT DEFAULT 'global_snowflake_seq') RETURNS BIGINT AS $$
DECLARE
  epoch bigint := 1716973200000;
  seq bigint;
  now_ms bigint;
  worker bigint := 1;
  result bigint;
BEGIN
  SELECT nextval(seq_name) % 1024 INTO seq;
  SELECT FLOOR(EXTRACT(EPOCH FROM clock_timestamp()) * 1000) INTO now_ms;
  result := (now_ms - epoch) << 23;
  result := result | (worker << 10);
  result := result | (seq);

  RETURN result;
END;
$$ LANGUAGE plpgsql;