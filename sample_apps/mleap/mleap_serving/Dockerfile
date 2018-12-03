FROM openjdk:8-jre-alpine
RUN mkdir -p /app
WORKDIR /app

COPY ./run_jar.sh ./target/scala-2.11/app-assembly.jar ./

RUN ["chmod", "+x", "./run_jar.sh"]

CMD ["./run_jar.sh"]