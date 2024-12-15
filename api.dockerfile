FROM openjdk:17-jdk-slim AS builder
WORKDIR /usr/app
COPY gradle gradle
COPY gradlew .
COPY build.gradle.kts .
COPY settings.gradle.kts .
COPY src src
RUN ./gradlew bootJar
RUN mv /usr/app/build/libs/api-0.0.1.jar /usr/app/api.jar
RUN mkdir -p /usr/morkato
ENTRYPOINT ["java", "-Dspring.profiles.active=prod,api", "-jar", "/usr/app/api.jar"]