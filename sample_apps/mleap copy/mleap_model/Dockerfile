ARG JDK_VERSION=openjdk:8-slim
ARG PYTHON_VERSION=3.7.0-slim

FROM ${JDK_VERSION} as model_trainer_jar_builder

WORKDIR /temp
COPY ./trainer /temp

ENV SPARK_VERSION=2.3.1
ENV HADOOP_VERSION=2.7
ENV SPARK_HOME=/temp/spark
ENV SBT_VERSION=1.2.7

# Install Spark
RUN apt-get update && apt-get install -y curl \
      && curl -O http://apache.mirror.iphh.net/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
      && tar -xvzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
      && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} spark \
      && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# Install Sbt and build jar
RUN curl -L -o sbt-${SBT_VERSION}.deb https://dl.bintray.com/sbt/debian/sbt-${SBT_VERSION}.deb \
      && dpkg -i sbt-${SBT_VERSION}.deb \
      && rm sbt-${SBT_VERSION}.deb \
      && apt-get update \
      && apt-get install sbt \
      && sbt clean assembly


FROM python:${PYTHON_VERSION} as deployer

WORKDIR /deploy
COPY . /deploy

# Copy jar into the correct location
COPY --from=model_trainer_jar_builder /temp/target/scala-2.11/mleap_model_trainer.jar /deploy/trainer/target/scala-2.11/

# Install any needed packages specified in requirements.txt
RUN apt-get update \
    && apt-get install -y autoconf=2.69-10 automake=1:1.15-6 build-essential=12.3 libtool=2.4.6-2 python-dev=2.7.13-2 jq=1.5+dfsg-1.3 \
    && make requirements \
    && chmod +x -R /deploy

CMD ["make", "deploy"]
