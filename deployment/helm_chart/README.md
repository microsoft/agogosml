# Kubernetes Helm Chart

## prerequisites

1. Install [Helm](https://helm.sh/)
2. Kubernetes cluster
3. Secret to the containers registry set as a [secret in kubernetes](https://kubernetes.io/docs/concepts/configuration/secret/)
4. Initialize Helm and Tiller
    - run: $helm init

## Installation

Install the chart using the 'helm install command'. provide different options using the -f command and supply a file with the updated settings. Example:

```bash
$ helm install . -f ../values.private.yaml
```

## Advanced usage

To control the blue/green deployment a simple update to the instance app service is needed.
change the label to either blue/green to redirect traffic:

```bash
TBD
```