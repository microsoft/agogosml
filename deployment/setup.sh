#!/bin/bash

# Following the tutorial found here:
# https://docs.microsoft.com/en-us/azure/terraform/terraform-create-k8s-cluster-with-tf-and-aks#set-up-azure-storage-to-store-terraform-state
# 
# More samples can be found here:
# https://github.com/terraform-providers/terraform-provider-azurerm/tree/master/examples

if [ ! -f ./tf.config.private.sh ]; then
    echo "tf.config.private.sh file not found!"
    exit 1
fi

. tf.config.private.sh

if [[ -z "${ARM_SUBSCRIPTION_ID}" ]]; then echo "ARM_SUBSCRIPTION_ID environment variable doesn't exists"; exit 1; fi
if [[ -z "${ARM_CLIENT_ID}" ]]; then echo "ARM_CLIENT_ID environment variable doesn't exists"; exit 1; fi
if [[ -z "${ARM_CLIENT_SECRET}" ]]; then echo "ARM_CLIENT_SECRET environment variable doesn't exists"; exit 1; fi
if [[ -z "${ARM_TENANT_ID}" ]]; then echo "ARM_TENANT_ID environment variable doesn't exists"; exit 1; fi
if [[ -z "${ARM_ENVIRONMENT}" ]]; then echo "ARM_ENVIRONMENT environment variable doesn't exists"; exit 1; fi
if [[ -z "${STORAGE_ACCOUNT_NAME}" ]]; then echo "STORAGE_ACCOUNT_NAME environment variable doesn't exists"; exit 1; fi
if [[ -z "${STORAGE_ACCOUNT_KEY}" ]]; then echo "STORAGE_ACCOUNT_KEY environment variable doesn't exists"; exit 1; fi
if [[ -z "${ARM_ACCESS_KEY}" ]]; then echo "ARM_ACCESS_KEY environment variable doesn't exists"; exit 1; fi

az storage container create -n tfstate --account-name $STORAGE_ACCOUNT_NAME --account-key $STORAGE_ACCOUNT_KEY
terraform init
terraform plan -out out.plan
terraform apply out.plan
