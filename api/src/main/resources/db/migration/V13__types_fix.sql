ALTER DOMAIN name_type
  DROP CONSTRAINT "name_type_check";
ALTER DOMAIN banner_type
  DROP CONSTRAINT "banner_type_check";
ALTER DOMAIN name_type
  ADD CONSTRAINT "name_type_check" CHECK (LENGTH(VALUE) >= 2 AND LENGTH(VALUE) <= 32 AND VALUE ~ '^[^:0-9\s\/][^:\/]{1,31}$');
ALTER DOMAIN banner_type
  ADD CONSTRAINT "banner_type_check" CHECK (VALUE ~ '^(https?://)(?:www\.)?[a-zA-Z0-9\-\.]{1,255}(?:/[a-zA-Z0-9\-\._~:\/?#\[\]@!$&''()*+,;=]{0,255})?|cdn://[0-9]{15,30}/[^:0-9\s\/]{2,32}$');