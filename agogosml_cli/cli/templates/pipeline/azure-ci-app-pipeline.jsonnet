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
                "+refs/heads/*"
            ],
            "forks": {
                "enabled": true,
                "allowSecrets": false
            },
            "pathFilters": [
                std.format("+/agogosml_cli/cli/templates/%s/%s", [std.extVar('PROJECT_NAME_SLUG'), std.extVar('PROJECT_NAME_SLUG')]),
            ],
            "isCommentRequiredForPullRequest": false,
            "triggerType": 64
        },
        {
            "branchFilters": [
                "+master"
            ],
            "pathFilters": [
                std.format("+/agogosml_cli/cli/templates/%s/%s", [std.extVar('PROJECT_NAME_SLUG'), std.extVar('PROJECT_NAME_SLUG')]),
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
                            "azureSubscriptionEndpoint": "FILL IN HERE",
                            "azureContainerRegistry": std.extVar('AZURE_CONTAINER_REGISTRY'),
                            "command": "Build an image",
                            "dockerFile": std.format("**/%s/Dockerfile.%s", [std.extVar('PROJECT_NAME_SLUG'), std.extVar('PROJECT_NAME_SLUG')]),
                            "arguments": std.extVar('AZURE_DOCKER_BUILDARGS'),
                            "useDefaultContext": "false",
                            "buildContext": std.format("agogosml_cli/cli/templates/%s/%s", [std.extVar('PROJECT_NAME_SLUG'), std.extVar('PROJECT_NAME_SLUG')]),
                            "pushMultipleImages": "false",
                            "tagMultipleImages": "false",
                            "imageName": "sample_app:$(Build.BuildId)",
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
                        "displayName": "Tag 'Latest'",
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
                            "script": "if [ $(Build.SourceBranchName) = \"master\" ]; then\n  echo \"Since this is a merge build, we are creating a new 'latest' tag\"\n  docker tag $(container_registry)/sample_app:$(Build.BuildId) $(container_registry)/sample_app:latest\n  echo \"Done\"\nelse\n  echo \"Not a merge build, hence skipping 'latest' tag\"\nfi\n",
                            "workingDirectory": "",
                            "failOnStderr": "false"
                        }
                    },
                    {
                        "environment": {},
                        "enabled": true,
                        "continueOnError": false,
                        "alwaysRun": false,
                        "displayName": "Push app image",
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
                            "azureSubscriptionEndpoint": "FILL IN HERE",
                            "azureContainerRegistry": std.extVar('AZURE_CONTAINER_REGISTRY'),
                            "command": "Push an image",
                            "dockerFile": "**/Dockerfile",
                            "arguments": "",
                            "useDefaultContext": "true",
                            "buildContext": "",
                            "pushMultipleImages": "false",
                            "tagMultipleImages": "false",
                            "imageName": "sample_app",
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
                "name": "agogosml-app-ci",
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
    "name": "agogosml-app-ci",
    "path": "\\",
    "type": 2
}