{
    "options": [],
    "triggers": [
        {
            "branchFilters": [
                "+master"
            ],
            "pathFilters": [
                "+/output_writer",
                "+/agogosml/agogosml"
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
                "+/output_writer",
                "+/agogosml/agogosml"
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
                        "displayName": "Docker compose: Build",
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
                            "azureSubscriptionEndpoint": "",
                            "azureContainerRegistry": "",
                            "dockerComposeFile": "**/generic_pipeline/output-app-docker-compose.yml",
                            "additionalDockerComposeFiles": "",
                            "dockerComposeFileArgs": "TAG=$(Build.BuildId)",
                            "projectName": "$(Build.Repository.Name)",
                            "qualifyImageNames": "true",
                            "action": "Build services",
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
                            "dockerComposeCommand": "build",
                            "dockerHostEndpoint": "",
                            "nopIfNoDockerComposeFile": "false",
                            "requireAdditionalDockerComposeFiles": "false",
                            "cwd": "$(System.DefaultWorkingDirectory)"
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
                            "azureSubscriptionEndpoint": "",
                            "azureContainerRegistry": "",
                            "command": "Push an image",
                            "dockerFile": "**/Dockerfile",
                            "arguments": "",
                            "useDefaultContext": "true",
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
                    }
                ],
                "name": "OutputWriter-Build-CI",
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
    "repository": {
        "properties": {},
        "clean": "true",
        "checkoutSubmodules": false
    },
    "processParameters": {},
    "quality": 1,
    "drafts": [],
    "id": 13,
    "name": "Output-Writer-Build-CI",
    "path": "\\",
    "type": 2
}