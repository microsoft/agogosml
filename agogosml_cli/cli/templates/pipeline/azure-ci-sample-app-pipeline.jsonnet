local repository = import 'pipeline-repository.libsonnet';

{
    "options": [],
    "triggers": [
        {
            "definition": {
                "id": 35,
                "url": "",
                "path": "\\",
                "queueStatus": 0,
                "project": {
                    "id": "0634c848-f8d0-4293-9c2a-570bab0d8457",
                    "name": std.extVar('PROJECT_NAME'),
                    "description": "Azure Pipelines for agogosml repo",
                    "url": "",
                    "state": 1,
                    "revision": 47,
                    "visibility": 2
                }
            },
            "requiresSuccessfulBuild": true,
            "branchFilters": [
                "+master"
            ],
            "triggerType": 128
        }
    ],
    "properties": {},
    "buildNumberFormat": "$(date:yyyyMMdd)$(rev:.r)",
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
                            "azureSubscriptionEndpoint": std.extVar('SUBSCRIPTION_ID'),
                            "azureContainerRegistry": std.extVar('AZURE_CONTAINER_REGISTRY'),
                            "command": "Build an image",
                            "dockerFile": "**/sample_app/Dockerfile.sample_app",
                            "arguments": std.extVar('AZURE_DOCKER_BUILDARGS'),
                            "useDefaultContext": "false",
                            "buildContext": "",
                            "pushMultipleImages": "false",
                            "tagMultipleImages": "false",
                            "imageName": "sample_app:$(Build.TriggeredBy.BuildId)",
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
                        "displayName": "Push instance app image",
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
                            "imageName": "sample_app:$(Build.TriggeredBy.BuildId)",
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
                "name": "Sample-App-Build-CI",
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
    "name": "Sample-App-Build-CI",
    "path": "\\",
    "type": 2
}