CREATE DOMAIN image_media_type AS VARCHAR(16) CHECK(VALUE ~ '^JPEG|PNG|GIF|WEBP$');
CREATE TABLE "images" (
  "author_id" discord_id_type NOT NULL,
  "name" name_type NOT NULL,
  "type" image_media_type NOT NULL,
  "file" TEXT NOT NULL
);

ALTER TABLE "images"
  ADD CONSTRAINT "image.pkey" PRIMARY KEY ("author_id","name");