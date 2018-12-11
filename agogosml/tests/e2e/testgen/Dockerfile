ARG CONTAINER_REG="agogosacr.azurecr.io/"
ARG AGOGOSML_TAG="939"

FROM ${CONTAINER_REG}agogosml:${AGOGOSML_TAG} as builder

# Copy the app
WORKDIR /usr/src/agogosml
COPY . ./testgen

# Release
FROM ${CONTAINER_REG}agogosml:${AGOGOSML_TAG} AS testgen

WORKDIR /testgen
COPY --from=builder /usr/src/agogosml/testgen /testgen

EXPOSE 5000

CMD ["python", "main.py"]
