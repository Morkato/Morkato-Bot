package morkato.api.infra.configuration

import org.springframework.context.annotation.Configuration
import org.springframework.context.annotation.Bean
import morkato.utils.MorkatoMetadataExtractor

@Configuration
class Utilities {
  val extractor = MorkatoMetadataExtractor()
  @Bean
  fun getMorkatoMetadataExtractor() : MorkatoMetadataExtractor {
    return extractor;
  }
}