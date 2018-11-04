# Terraform Deployment

# Prerequisites

- Make sure to run on bash or [Windows Bash](https://www.windowscentral.com/how-install-bash-shell-command-line-windows-10)
- [Create an SSH key on bash](https://docs.joyent.com/public-cloud/getting-started/ssh-keys/generating-an-ssh-key-manually/manually-generating-your-ssh-key-in-windows)
- Install [azure-cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- Install and configure [Terraform](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/terraform-install-configure)
- Make sure to run `az login` to run the deployment script
- Install the ask cli: `az aks install-cli`
- Copy `tf.config.sh` to `tf.config.private.sh` and update the values according to [Configuration Values](#configuration-values)
- Copy `variables.serviceprincipal.tf.example` to `variables.serviceprincipal.private.tf` and update `client_id` and `client_secret` with the service principal values

# Configuration Values

- ARM_SUBSCRIPTION_ID: Service principal subscription id
- ARM_CLIENT_ID: Service principal client id
- ARM_CLIENT_SECRET: Service principal secret
- ARM_TENANT_ID: Service principal tenant id
- ARM_ENVIRONMENT: Name of the environment (You can leave that as is)
- ARM_ACCESS_KEY: Storage account access key
- STORAGE_ACCOUNT_NAME: Storage account name for storing the terraform state