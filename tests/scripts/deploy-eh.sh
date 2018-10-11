#!/bin/bash

# Access granted under MIT Open Source License: https://en.wikipedia.org/wiki/MIT_License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, # and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions 
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED 
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.
#
#
# Description: Deploy ARM template which creates a Databricks account
#
# Usage: ./deploy.sh myResourceGroup "West Europe"
#
# Requirments:  
# - User must be logged in to the az cli with the appropriate account set.
# - User must have appropraite permission to deploy to a resource group
# - User must have appropriate permission to create a service principal

set -o errexit
set -o pipefail
set -o nounset
#set -o xtrace

# Constants
RED='\033[0;31m'
ORANGE='\033[0;33m'
NC='\033[0m'

###################
# SETUP

# Check if required utilities are installed
command -v jq >/dev/null 2>&1 || { echo >&2 "I require jq but it's not installed. See https://stedolan.github.io/jq/.  Aborting."; exit 1; }
command -v az >/dev/null 2>&1 || { echo >&2 "I require azure cli but it's not installed. See https://bit.ly/2Gc8IsS. Aborting."; exit 1; }

###################
# USER PARAMETERS

build_number="${1-}"

while [[ -z $build_number ]]; do
    read -rp "$(echo -e ${ORANGE}"Enter a prefix to the Event Hubs that should be created: "${NC})" build_number
done

# Creating the pipeline event hubs under the provided namespace
IFS=';' read -ra ehInstancesArray <<< "$EVENTHUBS_INSTANCES"
for ehName in "${ehInstancesArray[@]}"; do
    declare eh_name="${build_number}-${ehName}"
    echo "Creating event hub [${eh_name}] in event hub namespace [${EVENTHUBS_NAMESPACE}] in resource group [${RESOURCE_GROUP_NAME}]"
    declare result=$(az eventhubs eventhub create --resource-group "${RESOURCE_GROUP_NAME}" --namespace-name "${EVENTHUBS_NAMESPACE}" --name "${eh_name}")
done