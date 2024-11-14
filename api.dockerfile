FROM openjdk:17-jdk-slim AS builder
WORKDIR /usr/app
COPY gradle gradle
COPY gradlew .
COPY build.gradle.kts .
COPY settings.gradle.kts .
COPY src src
RUN ./gradlew bootJar
RUN mv /usr/app/build/libs/api-0.0.1.jar /usr/app/api.jar
RUN rm -r gradle
RUN rm -r .gradle
RUN rm -r build
RUN rm -r src
RUN rm gradlew
RUN rm build.gradle.kts
RUN rm settings.gradle.kts
ENTRYPOINT ["java", "-Dspring.profiles.active=prod", "-jar", "/usr/app/api.jar"]