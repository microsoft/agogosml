# Kubernetes Helm Chart

## prerequisites

1. Install [Helm](https://helm.sh/)
2. Kubernetes cluster
3. Initialize Helm and Tiller
    - run: $helm init

## Installation

Install the chart using the 'helm install command'. provide different options using the --set command. Example:

```bash
$ helm install . --set input-reader.tag=latest --set output_writer.tag=latest --set registry=myacr.azurecr.io
```