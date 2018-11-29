{
    "source": 2,
    "description": null,
    "isDeleted": false,
    "variables": {
        "agogosml_tag": {
            "value": "",
            "allowOverride": true
        },
        "System.Debug": {
            "value": "true"
        }
    },
    "variableGroups": [],
    "environments": [
        {
            "id": 6,
            "name": "Deploy chart",
            "rank": 1,
            "variables": {
                "app_host": {
                    "value": "0.0.0.0",
                    "allowOverride": true
                },
                "app_port": {
                    "value": "5000",
                    "allowOverride": true
                },
                "azure_storage_account": {
                    "value": "TBD",
                    "allowOverride": true
                },
                "event_hub_name": {
                    "value": "TBD",
                    "allowOverride": true
                },
                "event_hub_namespace": {
                    "value": "TBD",
                    "allowOverride": true
                },
                "event_hub_sas_key": {
                    "value": "TBD",
                    "allowOverride": true
                },
                "event_hub_sas_policy": {
                    "value": "TBD",
                    "allowOverride": true
                },
                "image_pull_secret": {
                    "value": "TBD",
                    "allowOverride": true
                },
                "kafka_address": {
                    "value": "TBD",
                    "allowOverride": true
                },
                "kafka_consumer_group": {
                    "value": "TBD",
                    "allowOverride": true
                },
                "kafka_topic": {
                    "value": "TBD",
                    "allowOverride": true
                },
                "lease_container_name": {
                    "value": "TBD",
                    "allowOverride": true
                },
                "messaging_type": {
                    "value": "TBD",
                    "allowOverride": true
                },
                "output_writer_port": {
                    "value": "TBD",
                    "allowOverride": true
                },
                "registry": {
                    "value": "TBD",
                    "allowOverride": true
                },
                "storage_access_key": {
                    "value": "TBD",
                    "allowOverride": true
                },
                "app_0_output_url": {
                    "value": "http://0.0.0.0:6000",
                    "allowOverride": true
                },
                "app_0_schema_filepath": {
                    "value": "schema_example.json",
                    "allowOverride": true
                }
            },
            "variableGroups": [],
            "preDeployApprovals": {
                "approvals": [
                    {
                        "rank": 1,
                        "isAutomated": true,
                        "isNotificationOn": false,
                        "id": 17
                    }
                ],
                "approvalOptions": {
                    "requiredApproverCount": null,
                    "releaseCreatorCanBeApprover": false,
                    "autoTriggeredAndPreviousEnvironmentApprovedCanBeSkipped": false,
                    "enforceIdentityRevalidation": false,
                    "timeoutInMinutes": 0,
                    "executionOrder": 1
                }
            },
            "deployStep": {
                "id": 22
            },
            "postDeployApprovals": {
                "approvals": [
                    {
                        "rank": 1,
                        "isAutomated": true,
                        "isNotificationOn": false,
                        "id": 23
                    }
                ],
                "approvalOptions": {
                    "requiredApproverCount": null,
                    "releaseCreatorCanBeApprover": false,
                    "autoTriggeredAndPreviousEnvironmentApprovedCanBeSkipped": false,
                    "enforceIdentityRevalidation": false,
                    "timeoutInMinutes": 0,
                    "executionOrder": 2
                }
            },
            "deployPhases": [
                {
                    "deploymentInput": {
                        "parallelExecution": {
                            "parallelExecutionType": 0
                        },
                        "skipArtifactsDownload": false,
                        "artifactsDownloadInput": {
                            "downloadInputs": [
                                {
                                    "alias": "_Agogosml__Git_Repo",
                                    "artifactType": "GitHub",
                                    "artifactDownloadMode": "All"
                                },
                                {
                                    "artifactItems": [],
                                    "alias": "_agogosml_instance_build",
                                    "artifactType": "Build",
                                    "artifactDownloadMode": "All"
                                }
                            ]
                        },
                        "queueId": 30,
                        "demands": [],
                        "enableAccessToken": false,
                        "timeoutInMinutes": 0,
                        "jobCancelTimeoutInMinutes": 1,
                        "condition": "succeeded()",
                        "overrideInputs": {}
                    },
                    "rank": 1,
                    "phaseType": 1,
                    "name": "Deploy Agogosml chart",
                    "refName": null,
                    "workflowTasks": [
                        {
                            "environment": {},
                            "taskId": "068d5909-43e6-48c5-9e01-7c8a94816220",
                            "version": "0.*",
                            "name": "Install Helm 2.10.0",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": false,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "helmVersion": "2.10.0",
                                "checkLatestHelmVersion": "true",
                                "installKubeCtl": "true",
                                "kubectlVersion": "1.8.9",
                                "checkLatestKubeCtl": "true"
                            }
                        },
                        {
                            "environment": {},
                            "taskId": "cbc316a2-586f-4def-be79-488a1f503564",
                            "version": "0.*",
                            "name": "kubectl get",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": false,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "kubernetesServiceEndpoint": "5a563e8b-1f86-486c-93d8-332ecfb50260",
                                "namespace": "",
                                "command": "get",
                                "useConfigurationFile": "false",
                                "configuration": "",
                                "arguments": "service",
                                "secretType": "dockerRegistry",
                                "secretArguments": "",
                                "containerRegistryType": "Azure Container Registry",
                                "dockerRegistryEndpoint": "",
                                "azureSubscriptionEndpoint": "",
                                "azureContainerRegistry": std.extVar('AZURE_CONTAINER_REGISTRY'),
                                "secretName": "",
                                "forceUpdate": "true",
                                "configMapName": "",
                                "forceUpdateConfigMap": "false",
                                "useConfigMapFile": "false",
                                "configMapFile": "",
                                "configMapArguments": "",
                                "versionOrLocation": "version",
                                "versionSpec": "1.7.0",
                                "checkLatest": "false",
                                "specifyLocation": "",
                                "cwd": "$(System.DefaultWorkingDirectory)",
                                "outputFormat": "yaml",
                                "kubectlOutput": "kubectl_service_output"
                            }
                        },
                        {
                            "environment": {},
                            "taskId": "cbc316a2-586f-4def-be79-488a1f503564",
                            "version": "0.*",
                            "name": "kubectl get",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": true,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "kubernetesServiceEndpoint": "5a563e8b-1f86-486c-93d8-332ecfb50260",
                                "namespace": "",
                                "command": "get",
                                "useConfigurationFile": "false",
                                "configuration": "",
                                "arguments": "deployment",
                                "secretType": "dockerRegistry",
                                "secretArguments": "",
                                "containerRegistryType": "Azure Container Registry",
                                "dockerRegistryEndpoint": "",
                                "azureSubscriptionEndpoint": "",
                                "azureContainerRegistry": std.extVar('AZURE_CONTAINER_REGISTRY'),
                                "secretName": "",
                                "forceUpdate": "true",
                                "configMapName": "",
                                "forceUpdateConfigMap": "false",
                                "useConfigMapFile": "false",
                                "configMapFile": "",
                                "configMapArguments": "",
                                "versionOrLocation": "version",
                                "versionSpec": "1.7.0",
                                "checkLatest": "false",
                                "specifyLocation": "",
                                "cwd": "$(System.DefaultWorkingDirectory)",
                                "outputFormat": "jsonpath='{.items[0].spec.template.spec.containers[0].image}'",
                                "kubectlOutput": "kubectl_deployment_output"
                            }
                        },
                        {
                            "environment": {},
                            "taskId": "6c731c3c-3c68-459a-a5c9-bde6e6595b5b",
                            "version": "3.*",
                            "name": "Bash Script",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": false,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "targetType": "inline",
                                "filePath": "",
                                "arguments": "",
                                "script": "echo \"$(kubectl_service_output)\" >> outputfile\nCOMMAND_SLOT1=`grep -o slot1 ./outputfile`\necho \"##vso[task.setvariable variable=slot1_found;]$COMMAND_SLOT1\"\n\nCOMMAND_SLOT2=`grep -o slot2 ./outputfile`\necho \"##vso[task.setvariable variable=slot2_found;]$COMMAND_SLOT2\"\n\necho \"$(kubectl_deployment_output)\" >> deploymentoutputfile\n#COMMAND_TAG=`grep image: ./deploymentoutputfile |sed 's/.*\\://'`\nCOMMAND_TAG=`echo $(kubectl_deployment_output) | sed 's/.*\\://'`\necho \"##vso[task.setvariable variable=deployment_tag;]$COMMAND_TAG\"",
                                "workingDirectory": "",
                                "failOnStderr": "false"
                            }
                        },
                        {
                            "environment": {},
                            "taskId": "6c731c3c-3c68-459a-a5c9-bde6e6595b5b",
                            "version": "3.*",
                            "name": "Bash Script - deployment selector",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": false,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "targetType": "inline",
                                "filePath": "",
                                "arguments": "",
                                "script": "# Option 1 - nothing is currently deployed\nif [[ \"$(slot1_found)\" = \"\" && \"$(slot2_found)\" = \"\" ]]; then\n  echo \"preparing for single deployment\"\n  echo \"##vso[task.setvariable variable=new_color]slot1\"\n  echo \"##vso[task.setvariable variable=slot1_enabled]true\"\n  echo \"##vso[task.setvariable variable=slot2_enabled]false\"\n  echo \"##vso[task.setvariable variable=slot1_tag]$(Release.Artifacts._agogosml_instance_build.BuildId)\"\n  echo \"##vso[task.setvariable variable=slot2_tag]none\"\nelif [[ \"$(slot1_found)\" = \"\" && \"$(slot2_found)\" = \"slot2\" ]]; then\n  echo \"##vso[task.setvariable variable=new_color]slot1\"\n  echo \"##vso[task.setvariable variable=slot2_enabled]true\"\n  echo \"##vso[task.setvariable variable=slot1_enabled]true\"\n  echo \"##vso[task.setvariable variable=slot1_tag]$(Release.Artifacts._agogosml_instance_build.BuildId)\"\n  echo \"##vso[task.setvariable variable=slot2_tag]$(deployment_tag)\"\nelif [[ \"$(slot1_found)\" = \"slot1\" && \"$(slot2_found)\" = \"\" ]]; then\n  echo \"##vso[task.setvariable variable=new_color]slot2\"\n  echo \"##vso[task.setvariable variable=slot2_enabled]true\"\n  echo \"##vso[task.setvariable variable=slot1_enabled]true\"\n  echo \"##vso[task.setvariable variable=slot1_tag]$(deployment_tag)\"\n  echo \"##vso[task.setvariable variable=slot2_tag]$(Release.Artifacts._agogosml_instance_build.BuildId)\"\nfi",
                                "workingDirectory": "",
                                "failOnStderr": "false"
                            }
                        },
                        {
                            "environment": {},
                            "taskId": "afa7d54d-537b-4dc8-b60a-e0eeea2c9a87",
                            "version": "0.*",
                            "name": "helm upgrade",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": false,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "connectionType": "Azure Resource Manager",
                                "azureSubscriptionEndpoint": "",
                                "azureResourceGroup": "agogosml-rg",
                                "kubernetesCluster": "agogosml-aks",
                                "kubernetesServiceEndpoint": "",
                                "namespace": "",
                                "command": "upgrade",
                                "chartType": "FilePath",
                                "chartName": "",
                                "chartPath": "$(System.DefaultWorkingDirectory)/_Agogosml__Git_Repo/deployment/helm_chart/agogosml",
                                "version": "",
                                "releaseName": "agogosml",
                                "overrideValues": "deployment=$(new_color),registry=$(registry),imagePullSecret=$(image_pull_secret),slot1.enabled=$(slot1_enabled),slot2.enabled=$(slot2_enabled),input_reader.tag=$(agogosml_tag),output_writer.tag=$(agogosml_tag),instance_apps.app_0.slot1_tag=$(slot1_tag),instance_apps.app_0.slot2_tag=$(slot2_tag),input_reader.env.MESSAGING_TYPE=$(messaging_type),input_reader.env.AZURE_STORAGE_ACCOUNT=$(azure_storage_account),input_reader.env.AZURE_STORAGE_ACCESS_KEY=$(storage_access_key),input_reader.env.EVENT_HUB_NAMESPACE=$(event_hub_namespace),input_reader.env.EVENT_HUB_NAME=$(event_hub_name),input_reader.env.EVENT_HUB_SAS_POLICY=$(event_hub_sas_policy),input_reader.env.EVENT_HUB_SAS_KEY=$(event_hub_sas_key),input_reader.env.LEASE_CONTAINER_NAME=$(lease_container_name),input_reader.env.KAFKA_TOPIC=$(kafka_topic),input_reader.env.KAFKA_CONSUMER_GROUP=$(kafka_consumer_group),input_reader.env.KAFKA_ADDRESS=$(kafka_address),output_writer.env.MESSAGING_TYPE=$(messaging_type),output_writer.env.EVENT_HUB_NAMESPACE=$(event_hub_namespace),output_writer.env.EVENT_HUB_NAME=$(event_hub_name),output_writer.env.EVENT_HUB_SAS_POLICY=$(event_hub_sas_policy),output_writer.env.EVENT_HUB_SAS_KEY=$(event_hub_sas_key),output_writer.env.KAFKA_TOPIC=$(kafka_topic),output_writer.env.KAFKA_ADDRESS=$(kafka_address),output_writer.env.OUTPUT_WRITER_PORT=$(output_writer_port),instance_apps.app_0.env.HOST=$(app_host),instance_apps.app_0.env.PORT=$(app_port),instance_apps.app_0.env.OUTPUT_URL=$(app_0_output_url),instance_apps.app_0.env.SCHEMA_FILEPATH=$(app_0_schema_filepath)",
                                "valueFile": "",
                                "destination": "$(Build.ArtifactStagingDirectory)",
                                "canaryimage": "false",
                                "upgradetiller": "true",
                                "updatedependency": "false",
                                "save": "true",
                                "install": "true",
                                "recreate": "false",
                                "resetValues": "false",
                                "force": "false",
                                "waitForExecution": "true",
                                "arguments": "",
                                "enableTls": "false",
                                "caCert": "",
                                "certificate": "",
                                "privatekey": "",
                                "tillernamespace": ""
                            }
                        }
                    ]
                }
            ],
            "environmentOptions": {
                "emailNotificationType": "OnlyOnFailure",
                "emailRecipients": "release.environment.owner;release.creator",
                "skipArtifactsDownload": false,
                "timeoutInMinutes": 0,
                "enableAccessToken": false,
                "publishDeploymentStatus": true,
                "badgeEnabled": false,
                "autoLinkWorkItems": false,
                "pullRequestDeploymentEnabled": false
            },
            "demands": [],
            "conditions": [],
            "executionPolicy": {
                "concurrencyCount": 1,
                "queueDepthCount": 0
            },
            "schedules": [],
            "retentionPolicy": {
                "daysToKeep": 10,
                "releasesToKeep": 3,
                "retainBuild": true
            },
            "processParameters": {},
            "properties": {},
            "preDeploymentGates": {
                "id": 0,
                "gatesOptions": null,
                "gates": []
            },
            "postDeploymentGates": {
                "id": 0,
                "gatesOptions": null,
                "gates": []
            },
            "environmentTriggers": []
        },
        {
            "id": 7,
            "name": "Approve",
            "rank": 2,
            "variables": {},
            "variableGroups": [],
            "preDeployApprovals": {
                "approvals": [
                    {
                        "rank": 1,
                        "isAutomated": true,
                        "isNotificationOn": false,
                        "id": 18
                    }
                ],
                "approvalOptions": {
                    "requiredApproverCount": null,
                    "releaseCreatorCanBeApprover": false,
                    "autoTriggeredAndPreviousEnvironmentApprovedCanBeSkipped": false,
                    "enforceIdentityRevalidation": false,
                    "timeoutInMinutes": 0,
                    "executionOrder": 1
                }
            },
            "deployStep": {
                "id": 21
            },
            "postDeployApprovals": {
                "approvals": [
                    {
                        "rank": 1,
                        "isAutomated": true,
                        "isNotificationOn": false,
                        "id": 24
                    }
                ],
                "approvalOptions": {
                    "requiredApproverCount": null,
                    "releaseCreatorCanBeApprover": false,
                    "autoTriggeredAndPreviousEnvironmentApprovedCanBeSkipped": false,
                    "enforceIdentityRevalidation": false,
                    "timeoutInMinutes": 0,
                    "executionOrder": 2
                }
            },
            "deployPhases": [
                {
                    "deploymentInput": {
                        "parallelExecution": {
                            "parallelExecutionType": 0
                        },
                        "skipArtifactsDownload": false,
                        "artifactsDownloadInput": {
                            "downloadInputs": [
                                {
                                    "alias": "_Agogosml__Git_Repo",
                                    "artifactType": "GitHub",
                                    "artifactDownloadMode": "All"
                                },
                                {
                                    "artifactItems": [],
                                    "alias": "_agogosml_instance_build",
                                    "artifactType": "Build",
                                    "artifactDownloadMode": "All"
                                }
                            ]
                        },
                        "queueId": 30,
                        "demands": [],
                        "enableAccessToken": false,
                        "timeoutInMinutes": 0,
                        "jobCancelTimeoutInMinutes": 1,
                        "condition": "succeeded()",
                        "overrideInputs": {}
                    },
                    "rank": 1,
                    "phaseType": 1,
                    "name": "Deploy Agogosml chart",
                    "refName": null,
                    "workflowTasks": [
                        {
                            "environment": {},
                            "taskId": "068d5909-43e6-48c5-9e01-7c8a94816220",
                            "version": "0.*",
                            "name": "Install Helm 2.10.0",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": false,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "helmVersion": "2.10.0",
                                "checkLatestHelmVersion": "true",
                                "installKubeCtl": "true",
                                "kubectlVersion": "1.8.9",
                                "checkLatestKubeCtl": "true"
                            }
                        },
                        {
                            "environment": {},
                            "taskId": "cbc316a2-586f-4def-be79-488a1f503564",
                            "version": "0.*",
                            "name": "kubectl get",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": false,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "kubernetesServiceEndpoint": "5a563e8b-1f86-486c-93d8-332ecfb50260",
                                "namespace": "",
                                "command": "get",
                                "useConfigurationFile": "false",
                                "configuration": "",
                                "arguments": "service",
                                "secretType": "dockerRegistry",
                                "secretArguments": "",
                                "containerRegistryType": "Azure Container Registry",
                                "dockerRegistryEndpoint": "",
                                "azureSubscriptionEndpoint": "",
                                "azureContainerRegistry": std.extVar('AZURE_CONTAINER_REGISTRY'),
                                "secretName": "",
                                "forceUpdate": "true",
                                "configMapName": "",
                                "forceUpdateConfigMap": "false",
                                "useConfigMapFile": "false",
                                "configMapFile": "",
                                "configMapArguments": "",
                                "versionOrLocation": "version",
                                "versionSpec": "1.7.0",
                                "checkLatest": "false",
                                "specifyLocation": "",
                                "cwd": "$(System.DefaultWorkingDirectory)",
                                "outputFormat": "yaml",
                                "kubectlOutput": "kubectl_service_output"
                            }
                        },
                        {
                            "environment": {},
                            "taskId": "6c731c3c-3c68-459a-a5c9-bde6e6595b5b",
                            "version": "3.*",
                            "name": "Bash Script",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": false,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "targetType": "inline",
                                "filePath": "",
                                "arguments": "",
                                "script": "echo \"$(kubectl_service_output)\" >> outputfile\nCOMMAND_SLOT1=`grep -o slot1 ./outputfile`\necho \"##vso[task.setvariable variable=slot1_found;]$COMMAND_SLOT1\"\n\nCOMMAND_SLOT2=`grep -o slot2 ./outputfile`\necho \"##vso[task.setvariable variable=slot2_found;]$COMMAND_SLOT2\"",
                                "workingDirectory": "",
                                "failOnStderr": "false"
                            }
                        },
                        {
                            "environment": {},
                            "taskId": "6c731c3c-3c68-459a-a5c9-bde6e6595b5b",
                            "version": "3.*",
                            "name": "Bash Script - deployment selector",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": false,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "targetType": "inline",
                                "filePath": "",
                                "arguments": "",
                                "script": "# Option 1 - slot2 is the current\nif [[ \"$(slot1_found)\" = \"\" && \"$(slot2_found)\" = \"slot2\" ]]; then\n  echo \"##vso[task.setvariable variable=slot2_enabled]true\"\n  echo \"##vso[task.setvariable variable=slot1_enabled]false\"\nelif [[ \"$(slot1_found)\" = \"slot1\" && \"$(slot2_found)\" = \"\" ]]; then\n  echo \"##vso[task.setvariable variable=slot2_enabled]false\"\n  echo \"##vso[task.setvariable variable=slot1_enabled]true\"\nfi",
                                "workingDirectory": "",
                                "failOnStderr": "false"
                            }
                        },
                        {
                            "environment": {},
                            "taskId": "afa7d54d-537b-4dc8-b60a-e0eeea2c9a87",
                            "version": "0.*",
                            "name": "helm upgrade",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": false,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "connectionType": "Azure Resource Manager",
                                "azureSubscriptionEndpoint": "",
                                "azureResourceGroup": "agogosml-rg",
                                "kubernetesCluster": "agogosml-aks",
                                "kubernetesServiceEndpoint": "",
                                "namespace": "",
                                "command": "upgrade",
                                "chartType": "FilePath",
                                "chartName": "",
                                "chartPath": "$(System.DefaultWorkingDirectory)/_Agogosml__Git_Repo/deployment/helm_chart/agogosml",
                                "version": "",
                                "releaseName": "agogosml",
                                "overrideValues": "slot1.enabled=$(slot1_enabled),slot2.enabled=$(slot2_enabled)",
                                "valueFile": "",
                                "destination": "$(Build.ArtifactStagingDirectory)",
                                "canaryimage": "false",
                                "upgradetiller": "true",
                                "updatedependency": "false",
                                "save": "true",
                                "install": "true",
                                "recreate": "false",
                                "resetValues": "false",
                                "force": "false",
                                "waitForExecution": "true",
                                "arguments": "--reuse-values",
                                "enableTls": "false",
                                "caCert": "",
                                "certificate": "",
                                "privatekey": "",
                                "tillernamespace": ""
                            }
                        }
                    ]
                }
            ],
            "environmentOptions": {
                "emailNotificationType": "OnlyOnFailure",
                "emailRecipients": "release.environment.owner;release.creator",
                "skipArtifactsDownload": false,
                "timeoutInMinutes": 0,
                "enableAccessToken": false,
                "publishDeploymentStatus": true,
                "badgeEnabled": false,
                "autoLinkWorkItems": false,
                "pullRequestDeploymentEnabled": false
            },
            "demands": [],
            "conditions": [],
            "executionPolicy": {
                "concurrencyCount": 1,
                "queueDepthCount": 0
            },
            "schedules": [],
            "retentionPolicy": {
                "daysToKeep": 10,
                "releasesToKeep": 3,
                "retainBuild": true
            },
            "processParameters": {},
            "properties": {},
            "preDeploymentGates": {
                "id": 0,
                "gatesOptions": null,
                "gates": []
            },
            "postDeploymentGates": {
                "id": 0,
                "gatesOptions": null,
                "gates": []
            },
            "environmentTriggers": []
        },
        {
            "id": 8,
            "name": "Reject",
            "rank": 3,
            "variables": {},
            "variableGroups": [],
            "preDeployApprovals": {
                "approvals": [
                    {
                        "rank": 1,
                        "isAutomated": true,
                        "isNotificationOn": false,
                        "id": 19
                    }
                ],
                "approvalOptions": {
                    "requiredApproverCount": null,
                    "releaseCreatorCanBeApprover": false,
                    "autoTriggeredAndPreviousEnvironmentApprovedCanBeSkipped": false,
                    "enforceIdentityRevalidation": false,
                    "timeoutInMinutes": 0,
                    "executionOrder": 1
                }
            },
            "deployStep": {
                "id": 20
            },
            "postDeployApprovals": {
                "approvals": [
                    {
                        "rank": 1,
                        "isAutomated": true,
                        "isNotificationOn": false,
                        "id": 25
                    }
                ],
                "approvalOptions": {
                    "requiredApproverCount": null,
                    "releaseCreatorCanBeApprover": false,
                    "autoTriggeredAndPreviousEnvironmentApprovedCanBeSkipped": false,
                    "enforceIdentityRevalidation": false,
                    "timeoutInMinutes": 0,
                    "executionOrder": 2
                }
            },
            "deployPhases": [
                {
                    "deploymentInput": {
                        "parallelExecution": {
                            "parallelExecutionType": 0
                        },
                        "skipArtifactsDownload": false,
                        "artifactsDownloadInput": {
                            "downloadInputs": [
                                {
                                    "alias": "_Agogosml__Git_Repo",
                                    "artifactType": "GitHub",
                                    "artifactDownloadMode": "All"
                                },
                                {
                                    "artifactItems": [],
                                    "alias": "_agogosml_instance_build",
                                    "artifactType": "Build",
                                    "artifactDownloadMode": "All"
                                }
                            ]
                        },
                        "queueId": 30,
                        "demands": [],
                        "enableAccessToken": false,
                        "timeoutInMinutes": 0,
                        "jobCancelTimeoutInMinutes": 1,
                        "condition": "succeeded()",
                        "overrideInputs": {}
                    },
                    "rank": 1,
                    "phaseType": 1,
                    "name": "Deploy Agogosml chart",
                    "refName": null,
                    "workflowTasks": [
                        {
                            "environment": {},
                            "taskId": "068d5909-43e6-48c5-9e01-7c8a94816220",
                            "version": "0.*",
                            "name": "Install Helm 2.10.0",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": false,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "helmVersion": "2.10.0",
                                "checkLatestHelmVersion": "true",
                                "installKubeCtl": "true",
                                "kubectlVersion": "1.8.9",
                                "checkLatestKubeCtl": "true"
                            }
                        },
                        {
                            "environment": {},
                            "taskId": "cbc316a2-586f-4def-be79-488a1f503564",
                            "version": "0.*",
                            "name": "kubectl get",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": false,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "kubernetesServiceEndpoint": "5a563e8b-1f86-486c-93d8-332ecfb50260",
                                "namespace": "",
                                "command": "get",
                                "useConfigurationFile": "false",
                                "configuration": "",
                                "arguments": "service",
                                "secretType": "dockerRegistry",
                                "secretArguments": "",
                                "containerRegistryType": "Azure Container Registry",
                                "dockerRegistryEndpoint": "",
                                "azureSubscriptionEndpoint": "",
                                "azureContainerRegistry": std.extVar('AZURE_CONTAINER_REGISTRY'),
                                "secretName": "",
                                "forceUpdate": "true",
                                "configMapName": "",
                                "forceUpdateConfigMap": "false",
                                "useConfigMapFile": "false",
                                "configMapFile": "",
                                "configMapArguments": "",
                                "versionOrLocation": "version",
                                "versionSpec": "1.7.0",
                                "checkLatest": "false",
                                "specifyLocation": "",
                                "cwd": "$(System.DefaultWorkingDirectory)",
                                "outputFormat": "yaml",
                                "kubectlOutput": "kubectl_service_output"
                            }
                        },
                        {
                            "environment": {},
                            "taskId": "6c731c3c-3c68-459a-a5c9-bde6e6595b5b",
                            "version": "3.*",
                            "name": "Bash Script",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": false,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "targetType": "inline",
                                "filePath": "",
                                "arguments": "",
                                "script": "echo \"$(kubectl_service_output)\" >> outputfile\nCOMMAND_SLOT1=`grep -o slot1 ./outputfile`\necho \"##vso[task.setvariable variable=slot1_found;]$COMMAND_SLOT1\"\n\nCOMMAND_SLOT2=`grep -o slot2 ./outputfile`\necho \"##vso[task.setvariable variable=slot2_found;]$COMMAND_SLOT2\"",
                                "workingDirectory": "",
                                "failOnStderr": "false"
                            }
                        },
                        {
                            "environment": {},
                            "taskId": "6c731c3c-3c68-459a-a5c9-bde6e6595b5b",
                            "version": "3.*",
                            "name": "Bash Script - deployment selector",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": false,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "targetType": "inline",
                                "filePath": "",
                                "arguments": "",
                                "script": "# Option 1 - slot2 is the current, revert and delete slot2\nif [[ \"$(slot1_found)\" = \"\" && \"$(slot2_found)\" = \"slot2\" ]]; then\n  echo \"##vso[task.setvariable variable=slot2_enabled]false\"\n  echo \"##vso[task.setvariable variable=slot1_enabled]true\"\n  echo \"##vso[task.setvariable variable=new_color]slot1\"\nelif [[ \"$(slot1_found)\" = \"slot1\" && \"$(slot2_found)\" = \"\" ]]; then\n  echo \"##vso[task.setvariable variable=slot2_enabled]true\"\n  echo \"##vso[task.setvariable variable=slot1_enabled]false\"\n  echo \"##vso[task.setvariable variable=new_color]slot2\"\nfi",
                                "workingDirectory": "",
                                "failOnStderr": "false"
                            }
                        },
                        {
                            "environment": {},
                            "taskId": "afa7d54d-537b-4dc8-b60a-e0eeea2c9a87",
                            "version": "0.*",
                            "name": "helm upgrade",
                            "refName": "",
                            "enabled": true,
                            "alwaysRun": false,
                            "continueOnError": false,
                            "timeoutInMinutes": 0,
                            "definitionType": "task",
                            "overrideInputs": {},
                            "condition": "succeeded()",
                            "inputs": {
                                "connectionType": "Azure Resource Manager",
                                "azureSubscriptionEndpoint": "",
                                "azureResourceGroup": "agogosml-rg",
                                "kubernetesCluster": "agogosml-aks",
                                "kubernetesServiceEndpoint": "",
                                "namespace": "",
                                "command": "upgrade",
                                "chartType": "FilePath",
                                "chartName": "",
                                "chartPath": "$(System.DefaultWorkingDirectory)/_Agogosml__Git_Repo/deployment/helm_chart/agogosml",
                                "version": "",
                                "releaseName": "agogosml",
                                "overrideValues": "slot1.enabled=$(slot1_enabled),slot2.enabled=$(slot2_enabled),deployment=$(new_color)",
                                "valueFile": "",
                                "destination": "$(Build.ArtifactStagingDirectory)",
                                "canaryimage": "false",
                                "upgradetiller": "true",
                                "updatedependency": "false",
                                "save": "true",
                                "install": "true",
                                "recreate": "false",
                                "resetValues": "false",
                                "force": "false",
                                "waitForExecution": "true",
                                "arguments": "--reuse-values",
                                "enableTls": "false",
                                "caCert": "",
                                "certificate": "",
                                "privatekey": "",
                                "tillernamespace": ""
                            }
                        }
                    ]
                }
            ],
            "environmentOptions": {
                "emailNotificationType": "OnlyOnFailure",
                "emailRecipients": "release.environment.owner;release.creator",
                "skipArtifactsDownload": false,
                "timeoutInMinutes": 0,
                "enableAccessToken": false,
                "publishDeploymentStatus": true,
                "badgeEnabled": false,
                "autoLinkWorkItems": false,
                "pullRequestDeploymentEnabled": false
            },
            "demands": [],
            "conditions": [],
            "executionPolicy": {
                "concurrencyCount": 1,
                "queueDepthCount": 0
            },
            "schedules": [],
            "retentionPolicy": {
                "daysToKeep": 10,
                "releasesToKeep": 3,
                "retainBuild": true
            },
            "processParameters": {},
            "properties": {},
            "preDeploymentGates": {
                "id": 0,
                "gatesOptions": null,
                "gates": []
            },
            "postDeploymentGates": {
                "id": 0,
                "gatesOptions": null,
                "gates": []
            },
            "environmentTriggers": []
        }
    ],
    "artifacts": [
        {
            "sourceId": "7030c884-91b4-4708-b5e9-cbda460e10ba:Microsoft/agogosml",
            "type": "GitHub",
            "alias": "_Agogosml__Git_Repo",
            "definitionReference": {
                "artifactSourceDefinitionUrl": {
                    "id": "https://github.com/Microsoft/agogosml",
                    "name": ""
                },
                "branch": {
                    "id": "master",
                    "name": "master"
                },
                "checkoutNestedSubmodules": {
                    "id": "True",
                    "name": "Any nested submodules within"
                },
                "checkoutSubmodules": {
                    "id": "",
                    "name": ""
                },
                "connection": {
                    "id": "7030c884-91b4-4708-b5e9-cbda460e10ba",
                    "name": "devlace"
                },
                "defaultVersionSpecific": {
                    "id": "",
                    "name": ""
                },
                "defaultVersionType": {
                    "id": "latestFromBranchType",
                    "name": "Latest from the default branch"
                },
                "definition": {
                    "id": "Microsoft/agogosml",
                    "name": "Microsoft/agogosml"
                },
                "fetchDepth": {
                    "id": "",
                    "name": ""
                },
                "gitLfsSupport": {
                    "id": "",
                    "name": ""
                }
            },
            "isPrimary": true,
            "isRetained": false
        },
        {
            "sourceId": "0634c848-f8d0-4293-9c2a-570bab0d8457:31",
            "type": "Build",
            "alias": "_agogosml_instance_build",
            "definitionReference": {
                "defaultVersionBranch": {
                    "id": "",
                    "name": ""
                },
                "defaultVersionSpecific": {
                    "id": "",
                    "name": ""
                },
                "defaultVersionTags": {
                    "id": "",
                    "name": ""
                },
                "defaultVersionType": {
                    "id": "selectDuringReleaseCreationType",
                    "name": "Specify at the time of release creation"
                },
                "definition": {
                    "id": "31",
                    "name": "Sample-app-build-CI (master)"
                },
                "definitions": {
                    "id": "",
                    "name": ""
                },
                "IsMultiDefinitionType": {
                    "id": "False",
                    "name": "False"
                },
                "project": {
                    "id": "0634c848-f8d0-4293-9c2a-570bab0d8457",
                    "name": "agogosml"
                },
                "repository": {
                    "id": "e6fc6b41-12c1-41f7-91be-c1369e61e5e0",
                    "name": "agogosml"
                }
            },
            "isRetained": false
        }
    ],
    "triggers": [],
    "releaseNameFormat": "rev-$(rev:r)",
    "tags": [],
    "properties": {
        "DefinitionCreationSource": {
            "$type": "System.String",
            "$value": "Other"
        }
    },
    "id": 2,
    "name": "agogosml-cd",
    "path": "\\",
    "projectReference": null
}