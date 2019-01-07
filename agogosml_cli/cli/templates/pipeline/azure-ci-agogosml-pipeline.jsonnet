local repository = import 'pipeline-repository.libsonnet';

{
    "options": [
        {
            "enabled": false,
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
    "triggers": [
        {
            "branchFilters": [
                "+master"
            ],
            "forks": {
                "enabled": false,
                "allowSecrets": false
            },
            "pathFilters": [
                "+/agogosml",
                "+/input_reader",
                "+/output_writer"
            ],
            "isCommentRequiredForPullRequest": false,
            "triggerType": 64
        },
        {
            "branchFilters": [
                "+master"
            ],
            "pathFilters": [
                "+/agogosml",
                "+/input_reader",
                "+/output_writer"
            ],
            "batchChanges": false,
            "maxConcurrentBuildsPerBranch": 1,
            "pollingInterval": 0,
            "triggerType": 2
        }
    ],
    "variables": {
        "container_registry": {
            "value": std.extVar('AZURE_CONTAINER_REGISTRY'),
            "allowOverride": true
        }
    },
    "properties": {},
    "buildNumberFormat": "$(date:yyyyMMdd)$(rev:.r)",
    "description": "Azure Pipelines for agogosml repo",
    "process": {
        "phases": [
            {
                "steps": [
                    {
                        "environment": {},
                        "enabled": true,
                        "continueOnError": false,
                        "alwaysRun": false,
                        "displayName": "Build an image",
                        "timeoutInMinutes": 0,
                        "condition": "succeeded()",
                        "task": {
                            "id": "e28912f1-0114-4464-802a-a3a35437fd16",
                            "versionSpec": "1.*",
                            "definitionType": "task"
                        },
                        "inputs": {
                            "containerregistrytype": "Azure Container Registry",
                            "dockerRegistryEndpoint": "",
                            "azureSubscriptionEndpoint": "",
                            "azureContainerRegistry": std.extVar('AZURE_CONTAINER_REGISTRY'),
                            "command": "Build an image",
                            "dockerFile": "**/agogosml/Dockerfile.agogosml",
                            "arguments": "",
                            "useDefaultContext": "true",
                            "buildContext": "",
                            "pushMultipleImages": "false",
                            "tagMultipleImages": "false",
                            "imageName": "agogosml:$(Build.BuildId)",
                            "imageNamesPath": "",
                            "qualifyImageName": "true",
                            "includeSourceTags": "false",
                            "includeLatestTag": "false",
                            "addDefaultLabels": "true",
                            "imageDigestFile": "",
                            "containerName": "",
                            "ports": "",
                            "volumes": "",
                            "envVars": "",
                            "workingDirectory": "",
                            "entrypointOverride": "",
                            "containerCommand": "",
                            "runInBackground": "true",
                            "restartPolicy": "no",
                            "maxRestartRetries": "",
                            "dockerHostEndpoint": "",
                            "enforceDockerNamingConvention": "true",
                            "memoryLimit": ""
                        }
                    },
                    {
                        "environment": {},
                        "enabled": true,
                        "continueOnError": false,
                        "alwaysRun": false,
                        "displayName": "Tag 'latest' tag",
                        "timeoutInMinutes": 0,
                        "condition": "succeeded()",
                        "task": {
                            "id": "6c731c3c-3c68-459a-a5c9-bde6e6595b5b",
                            "versionSpec": "3.*",
                            "definitionType": "task"
                        },
                        "inputs": {
                            "targetType": "inline",
                            "filePath": "",
                            "arguments": "",
                            "script": "if [ $(Build.SourceBranchName) = \"master\" ]; then\n  echo \"Since this is a merge build, we are creating a new 'latest' tag\"\n  docker tag $(container_registry)/agogosml:$(Build.BuildId) $(container_registry)/agogosml:latest\n  echo \"Done\"\nelse\n  echo \"Not a merge build, hence skipping 'latest' tag\"\nfi\n",
                            "workingDirectory": "",
                            "failOnStderr": "false"
                        }
                    },
                    {
                        "environment": {},
                        "enabled": true,
                        "continueOnError": false,
                        "alwaysRun": false,
                        "displayName": "Push base image",
                        "timeoutInMinutes": 0,
                        "condition": "succeeded()",
                        "task": {
                            "id": "e28912f1-0114-4464-802a-a3a35437fd16",
                            "versionSpec": "1.*",
                            "definitionType": "task"
                        },
                        "inputs": {
                            "containerregistrytype": "Azure Container Registry",
                            "dockerRegistryEndpoint": "",
                            "azureSubscriptionEndpoint": "",
                            "azureContainerRegistry": std.extVar('AZURE_CONTAINER_REGISTRY'),
                            "command": "Push an image",
                            "dockerFile": "**/agogosml/Dockerfile.agogosml",
                            "arguments": "",
                            "useDefaultContext": "true",
                            "buildContext": "",
                            "pushMultipleImages": "false",
                            "tagMultipleImages": "false",
                            "imageName": "agogosml",
                            "imageNamesPath": "",
                            "qualifyImageName": "true",
                            "includeSourceTags": "false",
                            "includeLatestTag": "false",
                            "addDefaultLabels": "true",
                            "imageDigestFile": "",
                            "containerName": "",
                            "ports": "",
                            "volumes": "",
                            "envVars": "",
                            "workingDirectory": "",
                            "entrypointOverride": "",
                            "containerCommand": "",
                            "runInBackground": "true",
                            "restartPolicy": "no",
                            "maxRestartRetries": "",
                            "dockerHostEndpoint": "",
                            "enforceDockerNamingConvention": "true",
                            "memoryLimit": ""
                        }
                    }
                ],
                "name": "Agogosml-Build-CI",
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
            },
            {
                "dependencies": [
                    {
                        "scope": "Phase_1",
                        "event": "Completed"
                    }
                ],
                "steps": [
                    {
                        "environment": {},
                        "enabled": true,
                        "continueOnError": false,
                        "alwaysRun": false,
                        "displayName": "Build an image",
                        "timeoutInMinutes": 0,
                        "condition": "succeeded()",
                        "task": {
                            "id": "e28912f1-0114-4464-802a-a3a35437fd16",
                            "versionSpec": "1.*",
                            "definitionType": "task"
                        },
                        "inputs": {
                            "containerregistrytype": "Azure Container Registry",
                            "dockerRegistryEndpoint": "",
                            "azureSubscriptionEndpoint": "",
                            "azureContainerRegistry": std.extVar('AZURE_CONTAINER_REGISTRY'),
                            "command": "Build an image",
                            "dockerFile": "**/input_reader/Dockerfile.input_reader",
                            "arguments": std.extVar('AZURE_DOCKER_BUILDARGS'),
                            "useDefaultContext": "false",
                            "buildContext": "",
                            "pushMultipleImages": "false",
                            "tagMultipleImages": "false",
                            "imageName": "input_reader:$(Build.BuildId)",
                            "imageNamesPath": "",
                            "qualifyImageName": "true",
                            "includeSourceTags": "false",
                            "includeLatestTag": "false",
                            "addDefaultLabels": "true",
                            "imageDigestFile": "",
                            "containerName": "",
                            "ports": "",
                            "volumes": "",
                            "envVars": "",
                            "workingDirectory": "",
                            "entrypointOverride": "",
                            "containerCommand": "",
                            "runInBackground": "true",
                            "restartPolicy": "no",
                            "maxRestartRetries": "",
                            "dockerHostEndpoint": "",
                            "enforceDockerNamingConvention": "true",
                            "memoryLimit": ""
                        }
                    },
                    {
                        "environment": {},
                        "enabled": true,
                        "continueOnError": false,
                        "alwaysRun": false,
                        "displayName": "Tag 'latest' tag",
                        "timeoutInMinutes": 0,
                        "condition": "succeeded()",
                        "task": {
                            "id": "6c731c3c-3c68-459a-a5c9-bde6e6595b5b",
                            "versionSpec": "3.*",
                            "definitionType": "task"
                        },
                        "inputs": {
                            "targetType": "inline",
                            "filePath": "",
                            "arguments": "",
                            "script": "if [ $(Build.SourceBranchName) = \"master\" ]; then\n  echo \"Since this is a merge build, we are creating a new 'latest' tag\"\n  docker tag $(container_registry)/input_reader:$(Build.BuildId) $(container_registry)/input_reader:latest\n  echo \"Done\"\nelse\n  echo \"Not a merge build, hence skipping 'latest' tag\"\nfi\n",
                            "workingDirectory": "",
                            "failOnStderr": "false"
                        }
                    },
                    {
                        "environment": {},
                        "enabled": true,
                        "continueOnError": false,
                        "alwaysRun": false,
                        "displayName": "Push input reader app image",
                        "timeoutInMinutes": 0,
                        "condition": "succeeded()",
                        "task": {
                            "id": "e28912f1-0114-4464-802a-a3a35437fd16",
                            "versionSpec": "1.*",
                            "definitionType": "task"
                        },
                        "inputs": {
                            "containerregistrytype": "Azure Container Registry",
                            "dockerRegistryEndpoint": "",
                            "azureSubscriptionEndpoint": std.extVar('SUBSCRIPTION_ID'),
                            "azureContainerRegistry": std.extVar('AZURE_CONTAINER_REGISTRY'),
                            "command": "Push an image",
                            "dockerFile": "**/Dockerfile",
                            "arguments": "",
                            "useDefaultContext": "true",
                            "buildContext": "",
                            "pushMultipleImages": "false",
                            "tagMultipleImages": "false",
                            "imageName": "input_reader",
                            "imageNamesPath": "",
                            "qualifyImageName": "true",
                            "includeSourceTags": "false",
                            "includeLatestTag": "false",
                            "addDefaultLabels": "true",
                            "imageDigestFile": "",
                            "containerName": "",
                            "ports": "",
                            "volumes": "",
                            "envVars": "",
                            "workingDirectory": "",
                            "entrypointOverride": "",
                            "containerCommand": "",
                            "runInBackground": "true",
                            "restartPolicy": "no",
                            "maxRestartRetries": "",
                            "dockerHostEndpoint": "",
                            "enforceDockerNamingConvention": "true",
                            "memoryLimit": ""
                        }
                    }
                ],
                "name": "InputReader-Build-CI",
                "refName": "Phase_2",
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
            },
            {
                "dependencies": [
                    {
                        "scope": "Phase_1",
                        "event": "Completed"
                    }
                ],
                "steps": [
                    {
                        "environment": {},
                        "enabled": true,
                        "continueOnError": false,
                        "alwaysRun": false,
                        "displayName": "Build an image",
                        "timeoutInMinutes": 0,
                        "condition": "succeeded()",
                        "task": {
                            "id": "e28912f1-0114-4464-802a-a3a35437fd16",
                            "versionSpec": "1.*",
                            "definitionType": "task"
                        },
                        "inputs": {
                            "containerregistrytype": "Azure Container Registry",
                            "dockerRegistryEndpoint": "",
                            "azureSubscriptionEndpoint": std.extVar('SUBSCRIPTION_ID'),
                            "azureContainerRegistry": std.extVar('AZURE_CONTAINER_REGISTRY'),
                            "command": "Build an image",
                            "dockerFile": "**/output_writer/Dockerfile.output_writer",
                            "arguments": std.extVar('AZURE_DOCKER_BUILDARGS'),
                            "useDefaultContext": "false",
                            "buildContext": "",
                            "pushMultipleImages": "false",
                            "tagMultipleImages": "false",
                            "imageName": "output_writer:$(Build.BuildId)",
                            "imageNamesPath": "",
                            "qualifyImageName": "true",
                            "includeSourceTags": "false",
                            "includeLatestTag": "false",
                            "addDefaultLabels": "true",
                            "imageDigestFile": "",
                            "containerName": "",
                            "ports": "",
                            "volumes": "",
                            "envVars": "",
                            "workingDirectory": "",
                            "entrypointOverride": "",
                            "containerCommand": "",
                            "runInBackground": "true",
                            "restartPolicy": "no",
                            "maxRestartRetries": "",
                            "dockerHostEndpoint": "",
                            "enforceDockerNamingConvention": "true",
                            "memoryLimit": ""
                        }
                    },
                    {
                        "environment": {},
                        "enabled": true,
                        "continueOnError": false,
                        "alwaysRun": false,
                        "displayName": "Tag 'latest' tag",
                        "timeoutInMinutes": 0,
                        "condition": "succeeded()",
                        "task": {
                            "id": "6c731c3c-3c68-459a-a5c9-bde6e6595b5b",
                            "versionSpec": "3.*",
                            "definitionType": "task"
                        },
                        "inputs": {
                            "targetType": "inline",
                            "filePath": "",
                            "arguments": "",
                            "script": "if [ $(Build.SourceBranchName) = \"master\" ]; then\n  echo \"Since this is a merge build, we are creating a new 'latest' tag\"\n  docker tag $(container_registry)/output_writer:$(Build.BuildId) $(container_registry)/output_writer:latest\n  echo \"Done\"\nelse\n  echo \"Not a merge build, hence skipping 'latest' tag\"\nfi\n",
                            "workingDirectory": "",
                            "failOnStderr": "false"
                        }
                    },
                    {
                        "environment": {},
                        "enabled": true,
                        "continueOnError": false,
                        "alwaysRun": false,
                        "displayName": "Push output writer app image",
                        "timeoutInMinutes": 0,
                        "condition": "succeeded()",
                        "task": {
                            "id": "e28912f1-0114-4464-802a-a3a35437fd16",
                            "versionSpec": "1.*",
                            "definitionType": "task"
                        },
                        "inputs": {
                            "containerregistrytype": "Azure Container Registry",
                            "dockerRegistryEndpoint": "",
                            "azureSubscriptionEndpoint": std.extVar('SUBSCRIPTION_ID'),
                            "azureContainerRegistry": std.extVar('AZURE_CONTAINER_REGISTRY'),
                            "command": "Push an image",
                            "dockerFile": "**/Dockerfile",
                            "arguments": "",
                            "useDefaultContext": "true",
                            "buildContext": "",
                            "pushMultipleImages": "false",
                            "tagMultipleImages": "false",
                            "imageName": "output_writer",
                            "imageNamesPath": "",
                            "qualifyImageName": "true",
                            "includeSourceTags": "false",
                            "includeLatestTag": "false",
                            "addDefaultLabels": "true",
                            "imageDigestFile": "",
                            "containerName": "",
                            "ports": "",
                            "volumes": "",
                            "envVars": "",
                            "workingDirectory": "",
                            "entrypointOverride": "",
                            "containerCommand": "",
                            "runInBackground": "true",
                            "restartPolicy": "no",
                            "maxRestartRetries": "",
                            "dockerHostEndpoint": "",
                            "enforceDockerNamingConvention": "true",
                            "memoryLimit": ""
                        }
                    }
                ],
                "name": "OutputWriter-Build-CI",
                "refName": "Phase_3",
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
    "id": 37,
    "name": "agogosml-ci",
    "path": "\\",
    "type": 2
}