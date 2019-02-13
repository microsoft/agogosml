ARG CONTAINER_REG_AGOGOSML
ARG TAG="latest"

FROM ${CONTAINER_REG_AGOGOSML}agogosml:${TAG} AS builder

# Copy the app
WORKDIR /usr/src/agogosml
COPY . ./testgen

# Add SSL Certificate 
RUN apk add ca-certificates

# Release
FROM ${CONTAINER_REG_AGOGOSML}agogosml:${TAG} AS testgen

WORKDIR /testgen
COPY --from=builder /usr/src/agogosml/testgen /testgen

CMD ["python", "main.py"]
