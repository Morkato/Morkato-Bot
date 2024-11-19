package morkato.api.dto.cdn

import java.io.InputStream
import java.nio.ByteBuffer
import java.nio.charset.Charset

data class CdnImageUploadHeaders(
  val authorId: Long,
  val imageName: String
) {
  companion object {
    private const val MAX_NAME_LENGTH = 32
    private const val STATIC_SIZE = 8 // authorId (Long): 8
    fun getHeadersFromBuffer(stream: InputStream) : CdnImageUploadHeaders {
      val authorIdBytes = ByteArray(8)
      if (stream.read(authorIdBytes) != 8) {
        throw RuntimeException()
      }
      val authorId = ByteBuffer.wrap(authorIdBytes).getLong()
      val lengthNameBytes = ByteArray(4)
      if (stream.read(lengthNameBytes) != 4) {
        throw RuntimeException()
      }
      val lengthName = ByteBuffer.wrap(lengthNameBytes).getInt()
      val imageNameBytes = ByteArray(lengthName)
      if (stream.read(imageNameBytes) != lengthName) {
        throw RuntimeException()
      }
      if (lengthName > MAX_NAME_LENGTH) {
        throw RuntimeException()
      }
      val imageName = String(imageNameBytes, Charset.forName("UTF-8"))
      return CdnImageUploadHeaders(authorId, imageName)
    }
  }
  fun size() : Int {
    return STATIC_SIZE + imageName.length
  }
}