package morkato.api

import org.springframework.boot.autoconfigure.jdbc.DataSourceTransactionManagerAutoConfiguration
import org.jetbrains.exposed.spring.autoconfigure.ExposedAutoConfiguration
import org.springframework.transaction.annotation.EnableTransactionManagement
import org.springframework.boot.autoconfigure.ImportAutoConfiguration
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication

@SpringBootApplication
@EnableTransactionManagement
@ImportAutoConfiguration(
  value = [ExposedAutoConfiguration::class],
  exclude = [DataSourceTransactionManagerAutoConfiguration::class]
)
class ApiApplication;
fun main(args: Array<String>) {
  runApplication<ApiApplication>(*args)
}
