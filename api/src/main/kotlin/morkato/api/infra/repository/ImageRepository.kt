package morkato.api.infra.repository

import morkato.api.exception.model.ImageNotFoundError
import org.jetbrains.exposed.sql.ResultRow
import morkato.api.infra.tables.images
import morkato.api.model.image.ImageType
import org.jetbrains.exposed.sql.selectAll
import org.jetbrains.exposed.sql.and
import org.jetbrains.exposed.sql.insert

object ImageRepository {
  public data class ImagePayload(
    val name: String,
    val type: ImageType,
    val authorId: String,
    val file: String
  ) {
    public constructor(row: ResultRow) : this(
      row[images.name],
      row[images.type],
      row[images.author_id],
      row[images.file]
    ) {}
  }
  fun findById(authorId: String, name: String) : ImagePayload {
    return try {
      ImagePayload(
        images.selectAll()
          .where({
            (images.author_id eq authorId)
              .and(images.name eq name)
          })
          .limit(1)
          .single()
      )
    } catch (exc: NoSuchElementException) {
      val data: MutableMap<String, Any?> = mutableMapOf()
      data["author_id"] = authorId
      data["name"] = name
      throw ImageNotFoundError(data)
    }
  }
  fun create(
    authorId: String,
    name: String,
    type: ImageType,
    file: String
  ) : ImagePayload {
    images.insert {
      it[this.author_id] = authorId
      it[this.name] = name
      it[this.type] = type
      it[this.file] = file
    }
    return ImagePayload(
      authorId = authorId,
      name = name,
      type = type,
      file = file
    )
  }
}