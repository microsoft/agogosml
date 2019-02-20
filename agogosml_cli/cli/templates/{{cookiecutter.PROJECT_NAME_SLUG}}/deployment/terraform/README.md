# Terraform Deployment

## Prerequisites

### Software 
- Bash: Make sure to run on bash or [Windows Bash](https://www.windowscentral.com/how-install-bash-shell-command-line-windows-10)
- Azure CLI: Install [azure-cli](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- Terraform: Install and configure [Terraform](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/terraform-install-configure)
- Kubectl: Install and set up [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl)

### Azure Permissions 

- First, login to Azure CLI: `az login`. Skip this step if you have already logged in.

- You *must* have `Owner` level role access to the Azure subscription. Run the command: `az role assignment list -o table` to view the account role assignment against Azure subscription(s). For example, in the output below only demo1 user has correct role assignment. 

    ```
    Principal                             Role         Scope
    ------------------------------------  -----------  ---------------------------------------------------
    demo1@contoso.com                     Owner        /subscriptions/1234-56789-1234543
    demo2@contoso.com                     Contributor  /subscriptions/1234-56789-1234543
    ```

## Select Appropriate Subscription
- List all Azure subscriptions by using the command: `az account list -o table`. Copy the `SubscriptionId` of subscription that you like to use for Terraform deployment. 

- Set a subscription to be the current active subscription: `az account set -s {SubscriptionId}`  

- Open `tf.config.private.sh` and update the value of `ARM_SUBSCRIPTION_ID` inside `tf.config.private.sh` with the `{SubscriptionId}`.

## Setup Terraform State Storage Account  

- Create a new Azure Resource Group using Azure CLI: `az group create -n az_tfstate_rg -l eastus`. You may want to change the location and group name based on your preference.

- Create a new Azure Storage account for storing the Terraform state: `az storage account create -n tfagogosml -g az_tfstate_rg -l eastus --sku Standard_LRS`

-  Read the Azure Storage account keys. Run the following command: `az storage account keys list -n tfagogosml -o table` and copy the value of either `key1` or `key2`. You will need this value later whenever reference to ARM_ACCESS_KEY is made.
    ```
    KeyName  Permissions     Value
    -----------------------------------------------
    key1       Full           *********************
    key2       Full           *********************
    ```
- Open `tf.config.private.sh` and update the value of `STORAGE_ACCOUNT_NAME` with `tfagogosml` and `ARM_ACCESS_KEY` with the relevant Azure Storage account key that you capture in the previous step. 

## Setup Azure AD Service Principal 

- Azure Kubernetes Service (AKS) requires a Service Principal with the Contributor level permissions. You are going to create a new Service Principal using Azure CLI. In the following command replace `{SUBSCRIPTION_ID}` with your Azure subscription id. 

    `az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/{SUBSCRIPTION_ID}" `

    > Note: You can list all the Azure subscriptions using `az account list -o table` command and then copy the value under the column 'SubscriptionId'

    You should see the output similar to the following (exact values may differ)
    ```
        {
        "appId": "435422f0-5f97-4aa9-8014-491b76f1e4c5",
        "displayName": "agogosml",
        "name": "http://agogosml",
        "password": "**********************",
        "tenant": "**************"
        }
    ```
- Open `tf.config.private.sh` and update following values based on the output above:
  `ARM_CLIENT_ID` with the value of `appId` 
  `ARM_CLIENT_SECRET` with the value of `password` 
  `ARM_TENANT_ID` with the value of `tenant`

- For AKS deployment, copy `variables.serviceprincipal.tf.example` to `variables.serviceprincipal.private.tf` and update `client_id` and `client_secret` with the service principal values.

# DeployResources Using Terraform

You can either deploy all the necessary Azure resources listed below at once, or individually.

* Azure Container Registry (ACR)
* Azure Kubernetes Service (AKS)
* Azure Storage 
* Azure Event Hub
* Azure Application Insights

Update preferred values in `variables.tf`, such as resource group name, and resource naming conventions. You may also want to inspect resource specifics values and update them based on your requirements. 

> Note: The default value for the resource group is `az_agogosml_rg` (where `az` is used as a prefix inside `variables.tf`). This means that all of the above Azure resources will reside in the same resource group. This also provides convenience from resource management standpoint.

- To run at once, run `. deployAllResources.sh`

- To run individually, `cd` into the resource's directory and run `. setup.sh`

# Destroy Resources Using Terraform

Use the following command to destroy individual resources.

- Azure Storage: `(cd ./azurestorage/ && terraform destroy -target=azurerm_storage_account.storage_account -auto-approve)`

- Azure Event Hub: `(cd ./eventhub/ && terraform destroy -target=azurerm_eventhub_namespace.eh -auto-approve)`

- Azure Container Service (ACR): `(cd ./acr/ && terraform destroy -target=azurerm_container_registry.acr -auto-approve)`

- Azure Kubernetes Service (AKS): `(cd ./aks/ && terraform destroy -target=azurerm_kubernetes_cluster.k8s -auto-approve)`

- Azure Application Insights: `(cd ./appinsights/ && terraform destroy -target=azurerm_application_insights.appinsights -auto-approve)`
 
# Troubleshooting 

- If you get permission denied error while executing `deployAllResources.sh` or `setup.sh` then try updating the file permissions: `sudo chmod 755 filename`

- Terraform maintains local state for each resource in addition to the remote state. Typically, you don't need to interact with local state  but in case you need to remove it (due to corruption etc.) you can do that by running following commands. Please note that this action is irreversible.

    * Azure Container Service (ACR): `rm ./acr/.terraform/terraform.tfstate` 
    * Azure Storage: `rm ./azurestorage/.terraform/terraform.tfstate` 
    * Azure Event Hub: `rm ./eventhub/.terraform/terraform.tfstate` 
    * Azure Kubernetes Service (AKS): `rm ./aks/.terraform/terraform.tfstate` 
    * Azure Application Insights: `rm ./appinsights/.terraform/terraform.tfstate`

# Configuration Values

- ARM_SUBSCRIPTION_ID: Service principal subscription id
- ARM_CLIENT_ID: Service principal client id
- ARM_CLIENT_SECRET: Service principal secret
- ARM_TENANT_ID: Service principal tenant id
- ARM_ENVIRONMENT: Name of the environment (You can leave that as is)
- ARM_ACCESS_KEY: Storage account access key
- STORAGE_ACCOUNT_NAME: Storage account name for storing the terraform state
