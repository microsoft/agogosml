# Start from Alpine and Java 8, and name this stage "build"
FROM openjdk:8u121-jre-alpine AS build
 
# Install SBT
ENV SBT_VERSION 0.13.15
ENV SBT_HOME /usr/local/sbt
ENV PATH ${PATH}:${SBT_HOME}/bin
RUN echo "installing SBT $SBT_VERSION" && \
apk add --no-cache --update bash wget && mkdir -p "$SBT_HOME" && \
wget -qO - --no-check-certificate "https://dl.bintray.com/sbt/native-packages/sbt/$SBT_VERSION/sbt-$SBT_VERSION.tgz" | tar xz -C $SBT_HOME --strip-components=1 && \
echo -ne "- with sbt $SBT_VERSION\n" >> /root/.built && \
sbt sbtVersion

# Set up the directory structure for our project
RUN mkdir -p /root/project-build/project
WORKDIR /root/project-build
 
# Resolve all our dependencies and plugins to speed up future compilations
# ADD ./project/plugins.sbt project/
ADD ./project/build.properties project/
ADD build.sbt .
RUN sbt update
 
# Add and compile our actual application source code
ADD . /mleap_serving
RUN sbt clean nativeLink
 
# Copy the binary executable to a consistent location
RUN cp ./target/scala-2.11/*-out ./project-build-out
 
# Start over from a clean Alpine image
FROM alpine:3.8
 
# Copy in the executable from "build"
COPY --from=build \
/root/project-build/project-build-out .
 
# Finally run the thing!
CMD ["./project-build-out"]