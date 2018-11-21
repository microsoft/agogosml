local repository = import 'pipeline-repository.libsonnet';

{
    "options": [],
    "triggers": [
        {
            "branchFilters": [
                "+refs/heads/master"
            ],
            "pathFilters": [
                "+/sample_app"
            ],
            "batchChanges": false,
            "maxConcurrentBuildsPerBranch": 1,
            "pollingInterval": 0,
            "triggerType": 2
        },
        {
            "branchFilters": [
                "+master"
            ],
            "forks": {
                "enabled": false,
                "allowSecrets": false
            },
            "pathFilters": [
                "+/sample_app"
            ],
            "isCommentRequiredForPullRequest": false,
            "triggerType": 64
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
                            "dockerFile": "**/sample_app/Dockerfile.app",
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
                "name": "App-Build-CI",
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
    "name": "App-Build-CI",
    "path": "\\",
    "type": 2
}