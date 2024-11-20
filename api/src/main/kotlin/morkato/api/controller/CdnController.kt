package morkato.api.controller

import jakarta.servlet.http.HttpServletResponse
import morkato.api.dto.validation.IdSchema
import morkato.api.dto.validation.NameSchema
import morkato.api.infra.repository.ImageRepository
import morkato.api.infra.service.MorkatoFileBukkit
import morkato.api.model.image.ImageType
import morkato.utils.MorkatoMetadataExtractor
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.context.annotation.Profile
import org.springframework.http.MediaType
import org.springframework.transaction.annotation.Transactional
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@Profile("cdn")
class CdnController(
  @Autowired val fileBukkit: MorkatoFileBukkit
) {
  @GetMapping("/{author_id}/{name}")
  @Transactional
  @Profile("api")
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