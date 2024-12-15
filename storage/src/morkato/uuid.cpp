#pragma once
#include <openssl/rand.h>
#include <string.h>
#include <iomanip>

void morkTransformUuidBase64(char** data, size_t length) {
  BIO* bio = BIO_new(BIO_s_mem());
  BIO* b64 = BIO_new(BIO_f_base64());
  BIO_set_flags(b64, BIO_FLAGS_BASE64_NO_NL);
  bio = BIO_push(b64, bio);
  BIO_write(bio, *data, length);
  BIO_flush(bio);
  char* encoded_data;
  long encoded_length = BIO_get_mem_data(bio, &encoded_data);
  *data = new char[encoded_length + 1];
  memcpy(*data, encoded_data, encoded_length);
  (*data)[encoded_length] = '\0';
  BIO_free_all(bio);
}

void morkGenerateUuid(char** id, const size_t& location, const size_t& register_loc) {
  int length = sizeof(size_t) * 2;
  *id = new char[length];
  memcpy(*id, &location, sizeof(size_t));
  memcpy(*id + sizeof(size_t), &register_loc, sizeof(size_t));
  morkTransformUuidBase64(id, length);
}
void morkExtractUuid(char* encoded_data, size_t* location, size_t* register_loc) {
  BIO* bio = BIO_new_mem_buf(encoded_data, strlen(encoded_data));
  BIO* b64 = BIO_new(BIO_f_base64());
  BIO_set_flags(b64, BIO_FLAGS_BASE64_NO_NL);
  bio = BIO_push(b64, bio);
  char buffer[16];
  int decoded_length = BIO_read(bio, buffer, sizeof(buffer));
  BIO_free_all(bio);
  memcpy(location, buffer, sizeof(size_t));
  memcpy(register_loc, buffer + sizeof(size_t), sizeof(size_t));
}