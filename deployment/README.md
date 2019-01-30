# Terraform Deployment

# Prerequisites

- Make sure to run on bash or [Windows Bash](https://www.windowscentral.com/how-install-bash-shell-command-line-windows-10)
- Install [azure-cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- If not already created, follow these instructions to create a [Service Principal in Azure:](https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli?view=azure-cli-latest#create-the-service-principal). You will need Contributor Access to your subscription.
- Install and configure [Terraform](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/terraform-install-configure)
- Make sure to run `az login` to run the deployment script
- Copy `tf.config.sh` to `tf.config.private.sh` and update the values
  according to [Configuration Values](#configuration-values)
- For AKS deployment, copy `variables.serviceprincipal.tf.example` to `variables.serviceprincipal.private.tf` and update `client_id` and `client_secret` with the service principal values
- Update preferred values in variables.tf, such as resource group name, and resource naming conventions.
- Now, you can either deploy all the necessary Azure resources at once, or deploy individually.
- To run at once, run `. deployAllResources.sh`
- To run individually, `cd` into the resource's directory and run `. setup.sh`

# Configuration Values

- ARM_SUBSCRIPTION_ID: Service principal subscription id
- ARM_CLIENT_ID: Service principal client id
- ARM_CLIENT_SECRET: Service principal secret
- ARM_TENANT_ID: Service principal tenant id
- ARM_ENVIRONMENT: Name of the environment (You can leave that as is)
- ARM_ACCESS_KEY: Storage account access key
- STORAGE_ACCOUNT_NAME: Storage account name for storing the terraform state
