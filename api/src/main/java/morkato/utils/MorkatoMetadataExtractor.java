package morkato.utils;

public class MorkatoMetadataExtractor {
  private static final byte[] JPEG1_SIGNATURE = new byte[3];
  private static final byte[] JPEG2_SIGNATURE = new byte[4];
  private static final byte[] JPEG3_SIGNATURE = new byte[3];
  private static final byte[] PNG_SIGNATURE = new byte[8];
  private static final byte[] GIF87A_SIGNATURE = new byte[6];
  private static final byte[] GIF89A_SIGNATURE = new byte[6];
  public static final int IMAGE_TOTAL_SIGNATURE_LENGTH = 8;
  static {
    // JPEG SIGNATURE 1: FF D8 FF
    JPEG1_SIGNATURE[0] = (byte) 0xFF;
    JPEG1_SIGNATURE[1] = (byte) 0xD8;
    JPEG1_SIGNATURE[2] = (byte) 0xFF;

    // JPEG SIGNATURE 2: FF D8 FF D8
    JPEG2_SIGNATURE[0] = (byte) 0xFF;
    JPEG2_SIGNATURE[1] = (byte) 0xD8;
    JPEG2_SIGNATURE[2] = (byte) 0xFF;
    JPEG2_SIGNATURE[3] = (byte) 0xDB;

    // JPEG SIGNATURE 3: FF D8 E0
    JPEG3_SIGNATURE[0] = (byte) 0xFF;
    JPEG3_SIGNATURE[1] = (byte) 0xD8;
    JPEG3_SIGNATURE[2] = (byte) 0xE0;

    // PNG SIGNATURE: 89 50 4E 47 0D 0A 1A 0A
    PNG_SIGNATURE[0] = (byte) 0x89;
    PNG_SIGNATURE[1] = (byte) 0x50;
    PNG_SIGNATURE[2] = (byte) 0x4E;
    PNG_SIGNATURE[3] = (byte) 0x47;
    PNG_SIGNATURE[4] = (byte) 0x0D;
    PNG_SIGNATURE[5] = (byte) 0x0A;
    PNG_SIGNATURE[6] = (byte) 0x1A;
    PNG_SIGNATURE[7] = (byte) 0x0A;

    // GIF87A SIGNATURE: 47 49 46 38 37 61
    GIF87A_SIGNATURE[0] = (byte) 0x47;
    GIF87A_SIGNATURE[1] = (byte) 0x49;
    GIF87A_SIGNATURE[2] = (byte) 0x46;
    GIF87A_SIGNATURE[3] = (byte) 0x38;
    GIF87A_SIGNATURE[4] = (byte) 0x37;
    GIF87A_SIGNATURE[5] = (byte) 0x61;

    // GIF89A SIGNATURE: 47 49 46 38 39 61
    GIF89A_SIGNATURE[0] = (byte) 0x47;
    GIF89A_SIGNATURE[1] = (byte) 0x49;
    GIF89A_SIGNATURE[2] = (byte) 0x46;
    GIF89A_SIGNATURE[3] = (byte) 0x38;
    GIF89A_SIGNATURE[4] = (byte) 0x39;
    GIF89A_SIGNATURE[5] = (byte) 0x61;
  }
  boolean checkSignature(byte[] buffer, byte[] signature) {
    if (buffer == null || buffer.length < signature.length) {
      return false;
    }
    for (int idx=0; idx<signature.length; ++idx) {
      if (buffer[idx] != signature[idx]) {
        return false;
      }
    }
    return true;
  }
  public boolean isJpeg1(byte[] buffer) {
    return checkSignature(buffer, JPEG1_SIGNATURE);
  }
  public boolean isJpeg2(byte[] buffer) {
    return checkSignature(buffer, JPEG2_SIGNATURE);
  }
  public boolean isJpeg3(byte[] buffer) {
    return checkSignature(buffer, JPEG3_SIGNATURE);
  }
  public boolean isJpeg(byte[] buffer) {
    return isJpeg1(buffer) || isJpeg2(buffer) || isJpeg3(buffer);
  }
  public boolean isPng(byte[] buffer) {
    return checkSignature(buffer, PNG_SIGNATURE);
  }
  public boolean isGif87a(byte[] buffer) {
    return checkSignature(buffer, GIF87A_SIGNATURE);
  }
  public boolean isGif89a(byte[] buffer) {
    return checkSignature(buffer, GIF89A_SIGNATURE);
  }
  public boolean isGif(byte[] buffer) {
    return isGif87a(buffer) || isGif89a(buffer);
  }
}