# Terraform Deployment

# Prerequisites

- Install [azure-cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- Install and configure [Terraform](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/terraform-install-configure)
- Make sure to run `az login` to run the deployment script
- Copy `tf.config.sh` to `tf.config.private.sh` and update the values according to [Configuration Values](#configuration-values)
- Update service principal values in `variables.tf`

# Configuration Values

- ARM_SUBSCRIPTION_ID: Service principal subscription id
- ARM_CLIENT_ID: Service principal client id
- ARM_CLIENT_SECRET: Service principal secret
- ARM_TENANT_ID: Service principal tenant id
- ARM_ENVIRONMENT: Name of the environment (You can leave that as is)
- ARM_ACCESS_KEY: Storage account access key
- STORAGE_ACCOUNT_NAME: Storage account name
- STORAGE_ACCOUNT_KEY: Storage account access key