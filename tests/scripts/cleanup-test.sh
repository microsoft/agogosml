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

###################
# SETUP

# Check if required utilities are installed
command -v jq >/dev/null 2>&1 || { echo >&2 "I require jq but it's not installed. See https://stedolan.github.io/jq/.  Aborting."; exit 1; }
command -v az >/dev/null 2>&1 || { echo >&2 "I require azure cli but it's not installed. See https://bit.ly/2Gc8IsS. Aborting."; exit 1; }

###################
# USER PARAMETERS

rg_name="${1-}"
eh_namespace="${2-}"
eh_prefix="${3-}"

while [[ -z $rg_name ]]; do
    read -rp "$(echo -e ${ORANGE}"Enter Resource Group name: "${NC})" rg_name
done

while [[ -z $eh_namespace ]]; do
    read -rp "$(echo -e ${ORANGE}"Enter Event Hubs Namespace name: "${NC})" eh_namespace
done

while [[ -z $eh_prefix ]]; do
    read -rp "$(echo -e ${ORANGE}"Enter a prefix to the Event Hubs that should be created: "${NC})" eh_prefix
done

for row in $(cat eventhubs.json | jq -r ".[] | .name"); do
  declare eh_name="${eh_prefix}-${row}"
  echo "Deleting event hub [${eh_name}] in event hub namespace [${eh_namespace}] in resource group [${rg_name}]"
  declare result=$(az eventhubs eventhub delete --resource-group "${rg_name}" --namespace-name "${eh_namespace}" --name "${eh_name}")
done