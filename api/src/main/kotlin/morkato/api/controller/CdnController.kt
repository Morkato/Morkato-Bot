package morkato.api.controller

import jakarta.servlet.http.HttpServletRequest
import jakarta.servlet.http.HttpServletResponse
import morkato.api.dto.cdn.CdnImageUploadHeaders
import morkato.api.dto.validation.IdSchema
import morkato.api.dto.validation.NameSchema
import morkato.api.exception.model.ImageNotFoundError
import morkato.api.infra.repository.ImageRepository
import morkato.api.infra.service.MorkatoFileBukkit
import morkato.api.model.image.ImageType
import morkato.utils.MorkatoMetadataExtractor
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.MediaType
import org.springframework.transaction.annotation.Transactional
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController
import java.io.BufferedInputStream
import java.io.InputStream

@RestController
@RequestMapping("/cdn")
class CdnController(
  @Autowired val extractor: MorkatoMetadataExtractor,
  @Autowired val fileBukkit: MorkatoFileBukkit
) {
  companion object {
    private const val MAX_IMAGE_LENGTH = 52428800 // 50MB
  }
  @PostMapping("/upload")
  @Transactional
  fun uploadImage(request: HttpServletRequest) : String {
    val stream = BufferedInputStream(request.getInputStream())
    val headers = CdnImageUploadHeaders.getHeadersFromBuffer(stream)
    val length = request.getHeader("Content-Length").toInt()
    val bodyLength = length - headers.size()
    if (bodyLength > MAX_IMAGE_LENGTH) {
      throw RuntimeException()
    }
    val otherImageRef = try {
      ImageRepository.findById(headers.authorId.toString(), headers.imageName)
    } catch (exc: ImageNotFoundError) { null }
    if (otherImageRef != null) {
      throw RuntimeException()
    }
    val imageHeaders = ByteArray(MorkatoMetadataExtractor.IMAGE_TOTAL_SIGNATURE_LENGTH)
    stream.read(imageHeaders)
    val type = when {
      extractor.isJpeg(imageHeaders) -> ImageType.JPEG
      extractor.isPng(imageHeaders) -> ImageType.PNG
      extractor.isGif(imageHeaders) -> ImageType.GIF
      else -> throw RuntimeException()
    }
    val body = imageHeaders + stream.readAllBytes()
    val id = fileBukkit.saveImage(body);
    ImageRepository.create(
      authorId = headers.authorId.toString(),
      name = headers.imageName,
      type = type,
      file = id
    )
    return id;
  }
  @GetMapping("/image/{author_id}/{name}")
  @Transactional
  fun getImage(
    @PathVariable("author_id") @IdSchema authorId: String,
    @PathVariable("name") @NameSchema name: String,
    response: HttpServletResponse
  ) : Unit {
    val image = ImageRepository.findById(authorId, name)
    val type = when (image.type) {
      ImageType.JPEG -> MediaType.IMAGE_JPEG
      ImageType.PNG -> MediaType.IMAGE_GIF
      ImageType.GIF -> MediaType.IMAGE_GIF
      else -> throw RuntimeException()
    }
    response.setContentType(type.toString())
    response.outputStream.write(fileBukkit.getImage(image.file).readAllBytes())
    response.outputStream.flush()
  }
}