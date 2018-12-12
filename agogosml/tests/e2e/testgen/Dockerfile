ARG CONTAINER_REG
ARG TAG

FROM ${CONTAINER_REG}agogosml:${TAG} as builder

# Copy the app
WORKDIR /usr/src/agogosml
COPY . ./testgen

# Release
FROM ${CONTAINER_REG}agogosml:${TAG} AS testgen

WORKDIR /testgen
COPY --from=builder /usr/src/agogosml/testgen /testgen

CMD ["python", "main.py"]
