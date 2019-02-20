#!/bin/bash

# Run the setup scripts for each resource. 

if [ ! -f ./tf.config.private.sh ]; then
    echo "tf.config.private.sh file not found!"
    exit 1
fi

# Load environment variables defined by user
. ./tf.config.private.sh

# Check for an environment variable name if it exists and exit if not
check_variable_exists () {
    declare variable_name="$1"
    declare variable_value=$(printf '%s\n' "${!variable_name}")
    if [[ -z "${variable_value}" ]]; then
        echo "${variable_name} environment variable doesn't exists";
        exit 1;
    fi
}

check_variable_exists "ARM_SUBSCRIPTION_ID"
check_variable_exists "ARM_CLIENT_ID"
check_variable_exists "ARM_CLIENT_SECRET"
check_variable_exists "ARM_TENANT_ID"
check_variable_exists "ARM_ENVIRONMENT"
check_variable_exists "STORAGE_ACCOUNT_NAME"
check_variable_exists "ARM_ACCESS_KEY"

# The tfstate file will be upload to azure storage to maintain consistency and future destruction of the resources.
az storage container create -n tfstate --account-name $STORAGE_ACCOUNT_NAME --account-key $ARM_ACCESS_KEY
# Create ACR
echo "About to create the ACR Terraform Plan"
(cd ./acr && ./setup.sh)
echo "Completed deploying ACR"

# Create Azure Storage
echo "About to create the Azure Storage Terraform Plan"
(cd ./azurestorage && ./setup.sh)
echo "Completed deploying Azure Storage"

# Create Event Hub
echo "About to create the Eventhub Terraform Plan"
(cd ./eventhub && ./setup.sh)
echo "Completed deploying Eventhub"

# Create AKS 
echo "About to create the AKS Plan"
(cd ./aks && ./setup.sh)
echo "Completed deploying AKS"

# Create Application Insights
echo "About to create the Application Insights Plan"
(cd ./appinsights && ./setup.sh)
echo "Completed deploying Application Insights"
