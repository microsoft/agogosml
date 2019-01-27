#!/bin/bash

# Run the setup scripts for each resource. 

# Create ACR
. acr/setup.sh

# Create Azure Storage
. azurestorage/setup.sh

# Create Event Hub
. eventhub/setup.sh

# Create AKS 
. aks/setup.sh

