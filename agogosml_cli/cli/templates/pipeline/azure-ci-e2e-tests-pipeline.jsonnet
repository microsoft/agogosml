local repository = import 'pipeline-repository.libsonnet';

{
    "options": [
        {
            "enabled": true,
            "definition": {
                "id": "5d58cc01-7c75-450c-be18-a388ddb129ec"
            },
            "inputs": {
                "branchFilters": "[\"+refs/heads/*\"]",
                "additionalFields": "{}"
            }
        },
        {
            "enabled": false,
            "definition": {
                "id": "a9db38f9-9fdc-478c-b0f9-464221e58316"
            },
            "inputs": {
                "workItemType": "3060103",
                "assignToRequestor": "true",
                "additionalFields": "{}"
            }
        }
    ],
    "variables": {
        "agogosml_tag": {
            "value": "latest",
            "allowOverride": true
        },
        "app_tag": {
            "value": "latest",
            "allowOverride": true
        },
        "azure_storage_access_key": {
            "value": "",
            "allowOverride": true
        },
        "azure_storage_account": {
            "value": "",
            "allowOverride": true
        },
        "container_registry": {
            "value": std.extVar('AZURE_CONTAINER_REGISTRY'),
            "allowOverride": true
        },
        "eh_sas_key_input": {
            "value": "",
            "allowOverride": true
        },
        "eh_sas_key_output": {
            "value": "",
            "allowOverride": true
        },
        "event_hub_name_input": {
            "value": "",
            "allowOverride": true
        },
        "event_hub_name_output": {
            "value": "",
            "allowOverride": true
        },
        "event_hub_namespace": {
            "value": "",
            "allowOverride": true
        },
        "event_hub_sas_policy": {
            "value": "",
            "allowOverride": true
        },
        "lease_container_name_input": {
            "value": "",
            "allowOverride": true
        },
        "lease_container_name_output": {
            "value": "",
            "allowOverride": true
        },
        "messaging_type": {
            "value": "",
            "allowOverride": true
        },
        "system.debug": {
            "value": "false",
            "allowOverride": true
        }
    },
    "retentionRules": [
        {
            "branches": [
                "+refs/heads/*"
            ],
            "artifacts": [],
            "artifactTypesToDelete": [
                "FilePath",
                "SymbolStore"
            ],
            "daysToKeep": 10,
            "minimumToKeep": 1,
            "deleteBuildRecord": true,
            "deleteTestResults": true
        }
    ],
    "properties": {},
    "tags": [],
    "buildNumberFormat": "$(date:yyyyMMdd)$(rev:.r)",
    "jobAuthorizationScope": 1,
    "jobTimeoutInMinutes": 60,
    "jobCancelTimeoutInMinutes": 5,
    "badgeEnabled": true,
    "process": {
        "phases": [
            {
                "steps": [
                    {
                        "environment": {},
                        "enabled": true,
                        "continueOnError": false,
                        "alwaysRun": false,
                        "displayName": "Run a Docker Compose command",
                        "timeoutInMinutes": 0,
                        "condition": "succeeded()",
                        "task": {
                            "id": "6975e2d1-96d3-4afc-8a41-498b5d34ea19",
                            "versionSpec": "0.*",
                            "definitionType": "task"
                        },
                        "inputs": {
                            "containerregistrytype": "Azure Container Registry",
                            "dockerRegistryEndpoint": "",
                            "azureSubscriptionEndpoint": std.extVar('SUBSCRIPTION_ID'),
                            "azureContainerRegistry": std.extVar('AZURE_CONTAINER_REGISTRY'),
                            "dockerComposeFile": "**/docker-compose-agogosml.yml",
                            "additionalDockerComposeFiles": "docker-compose-testgen.yml",
                            "dockerComposeFileArgs": "CONTAINER_REG=$(container_registry)\nAZURE_STORAGE_ACCESS_KEY=$(azure_storage_access_key)\nEVENT_HUB_SAS_KEY_INPUT=$(eh_sas_key_input)\nEVENT_HUB_SAS_KEY_OUTPUT=$(eh_sas_key_output)\nTAG=$(agogosml_tag)\nAPP_TAG=$(app_tag)\nAZURE_STORAGE_ACCOUNT=$(azure_storage_account)\nEVENT_HUB_NAME_INPUT=$(event_hub_name_input)\nEVENT_HUB_NAME_OUTPUT=$(event_hub_name_output)\nLEASE_CONTAINER_NAME_OUTPUT=$(lease_container_name_output)\nLEASE_CONTAINER_NAME_INPUT=$(lease_container_name_input)\nEVENT_HUB_NAMESPACE=$(event_hub_namespace)\nEVENT_HUB_SAS_POLICY=$(event_hub_sas_policy)\nMESSAGING_TYPE=$(messaging_type)",
                            "projectName": "$(Build.Repository.Name)",
                            "qualifyImageNames": "true",
                            "action": "Run a Docker Compose command",
                            "additionalImageTags": "",
                            "includeSourceTags": "false",
                            "includeLatestTag": "false",
                            "buildImages": "true",
                            "serviceName": "",
                            "containerName": "",
                            "ports": "",
                            "workDir": "",
                            "entrypoint": "",
                            "containerCommand": "",
                            "detached": "true",
                            "abortOnContainerExit": "true",
                            "imageDigestComposeFile": "$(Build.StagingDirectory)/docker-compose.images.yml",
                            "removeBuildOptions": "false",
                            "baseResolveDirectory": "",
                            "outputDockerComposeFile": "$(Build.StagingDirectory)/docker-compose.yml",
                            "dockerComposeCommand": "up  --exit-code-from tester-gen",
                            "dockerHostEndpoint": "",
                            "nopIfNoDockerComposeFile": "false",
                            "requireAdditionalDockerComposeFiles": "true",
                            "cwd": "$(System.DefaultWorkingDirectory)"
                        }
                    }
                ],
                "name": "Agent job 1",
                "refName": "Phase_1",
                "condition": "succeeded()",
                "target": {
                    "executionOptions": {
                        "type": 0
                    },
                    "allowScriptsAuthAccessOption": false,
                    "type": 1
                },
                "jobAuthorizationScope": 1,
                "jobCancelTimeoutInMinutes": 1
            }
        ],
        "type": 1
    },
    "repository": repository.Repository(std.extVar('REPOSITORY_TYPE'), std.extVar('REPOSITORY_URL'), std.extVar('REPOSITORY_OWNER'), std.extVar('REPOSITORY_REPO')),
    "processParameters": {},
    "quality": 1,
    "drafts": [],
    "name": "agogosml-E2E tests",
    "path": "\\",
    "type": 2,
    "queueStatus": 0
}