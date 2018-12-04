ARG JDK_VERSION=openjdk:8-jre-alpine

FROM ${JDK_VERSION} as jar_builder

WORKDIR /temp
COPY . /temp

ARG SBT_VERSION=1.2.7

RUN apk update && apk add ca-certificates wget tar bash && \
    mkdir -p "/usr/local/sbt" && \
    wget -qO - --no-check-certificate "https://piccolo.link/sbt-${SBT_VERSION}.tgz" > sbt-${SBT_VERSION}.tgz && \
    tar --extract --file "sbt-${SBT_VERSION}.tgz" --directory "/usr/local/sbt" --strip-components 1

RUN ["/usr/local/sbt/bin/sbt", "assembly"]

FROM ${JDK_VERSION}

ARG SCALA_VERSION=2.11

WORKDIR /app
COPY --from=jar_builder /temp/run_jar.sh /app
COPY --from=jar_builder /temp/target/scala-${SCALA_VERSION}/app-assembly.jar /app
COPY --from=jar_builder /temp/assets/sample_model.zip /app

RUN ["chmod", "+x", "./run_jar.sh"]

CMD ["./run_jar.sh"]