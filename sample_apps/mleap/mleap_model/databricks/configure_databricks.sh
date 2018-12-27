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
# Description: Deploy Databricks cluster
#
# Usage: 
#
# Requirments:  
#

set -o errexit
set -o pipefail
set -o nounset
# set -o xtrace

# Set path
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

# Constants
RED='\033[0;31m'
ORANGE='\033[0;33m'
NC='\033[0m'

cluster_config="./config/cluster.config.json"

wait_for_run () {
    # See here: https://docs.azuredatabricks.net/api/latest/jobs.html#jobsrunresultstate
    declare mount_run_id=$1
    while : ; do
        life_cycle_status=$(databricks runs get --run-id $mount_run_id | jq -r ".state.life_cycle_state") 
        result_state=$(databricks runs get --run-id $mount_run_id | jq -r ".state.result_state")
        if [[ $result_state == "SUCCESS" || $result_state == "SKIPPED" ]]; then
            break;
        elif [[ $life_cycle_status == "INTERNAL_ERROR" || $result_state == "FAILED" ]]; then
            state_message=$(databricks runs get --run-id $mount_run_id | jq -r ".state.state_message")
            echo -e "${RED}Error while running ${mount_run_id}: ${state_message} ${NC}"
            exit 1
        else 
            echo "Waiting for run ${mount_run_id} to finish..."
            sleep 2m
        fi
    done
}

cluster_exists () {
    declare cluster_name="$1"
    declare cluster=$(databricks clusters list | tr -s " " | cut -d" " -f2 | grep ^${cluster_name}$)
    if [[ -n $cluster ]]; then
        return 0; # cluster exists
    else
        return 1; # cluster does not exists
    fi
}

yes_or_no () {
    while true; do
        read -p "$(echo -e ${ORANGE}"$* [y/n]: "${NC})" yn
        case $yn in
            [Yy]*) return 0  ;;  
            [Nn]*) echo -e "${RED}Aborted${NC}" ; return  1 ;;
        esac
    done
}


_main() {
    echo -e "${ORANGE}"
    echo -e "!! -- WARNING --!!"
    echo -e "If this is the second time you are running this, this will re-upload and overwrite existing notebooks with the same names in the 'notebooks' folder. "
    echo -e "This will also drop and reload data in Tables."
    echo -e "${NC}"
    yes_or_no "Are you sure you want to continue (Y/N)?" || { exit 1; }

    # Upload notebooks
    echo "Uploading notebooks..."
    databricks workspace import_dir "./notebooks" "/agogos" --overwrite

    # Setup workspace
    echo "Mounting blob storage. This may take a while as cluster spins up..."
    wait_for_run $(databricks runs submit --json-file "./config/run.mountblob.config.json" | jq -r ".run_id" )

    # Create initial cluster, if not yet exists
    echo "Creating an interactive cluster..."
    cluster_name=$(cat $cluster_config | jq -r ".cluster_name")
    if cluster_exists $cluster_name; then 
        echo "Cluster ${cluster_name} already exists!"
    else
        echo "Creating cluster ${cluster_name}..."
        databricks clusters create --json-file $cluster_config
    fi

    # Install Library
    echo "Installing libraries..."
    cluster_id=$(databricks clusters list | awk '/'$cluster_name'/ {print $1}')

    # Install jar on cluster - this jar was uploaded as part of deploy_resources.sh
    databricks libraries install --jar dbfs:/mnt/blob_storage/modeljars/mleap_model_trainer.jar --cluster-id $cluster_id
}

_main
