plugins {
  kotlin("jvm") version "1.9.25"
  kotlin("plugin.spring") version "1.9.25"
  id("org.springframework.boot") version "3.3.3"
  id("io.spring.dependency-management") version "1.1.6"
}

group = "morkato"
version = "0.0.1"

java {
  toolchain {
    languageVersion = JavaLanguageVersion.of(17)
  }
}

repositories {
  mavenCentral()
}

dependencies {
  implementation("org.springframework.boot:spring-boot-starter-jdbc")
  implementation("org.springframework.boot:spring-boot-starter-validation")
  implementation("org.springframework.boot:spring-boot-starter-web")
  implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
  implementation("org.jetbrains.exposed:exposed-spring-boot-starter:0.54.0")
  implementation("org.jetbrains.exposed:exposed-core:0.54.0")
  implementation("org.jetbrains.exposed:exposed-dao:0.54.0")
  implementation("org.jetbrains.exposed:exposed-jdbc:0.54.0")
  implementation("org.jetbrains.exposed:exposed-java-time:0.54.0")
  implementation("org.flywaydb:flyway-core")
  implementation("org.flywaydb:flyway-database-postgresql:10.0.0")
  implementation("org.jetbrains.kotlin:kotlin-reflect")
  runtimeOnly("org.postgresql:postgresql")
  testImplementation("org.springframework.boot:spring-boot-starter-test")
  testImplementation("org.jetbrains.kotlin:kotlin-test-junit5")
  testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

kotlin {
  compilerOptions {
    freeCompilerArgs.addAll("-Xjsr305=strict")
  }
}

tasks.withType<Test> {
  useJUnitPlatform()
}

tasks.bootJar {
  duplicatesStrategy = DuplicatesStrategy.EXCLUDE
  mainClass.set("morkato.api.ApiApplicationKt")
  
}
