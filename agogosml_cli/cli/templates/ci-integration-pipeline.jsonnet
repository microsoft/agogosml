{
    "options": [],
    "triggers": [
        {
            "pollingInterval": 0,
            "triggerType": 2
        },
        {
            "definition": {
                "id": 19,
                "path": "\\",
                "queueStatus": 0,
                "project": {
                    "name": std.extVar('PROJECT_NAME'),
                    "description": "Integration CI pipeline",
                    "state": 1,
                    "visibility": "public"
                }
            },
            "requiresSuccessfulBuild": true,
            "branchFilters": [
                "+azure-pipelines-build"
            ],
            "triggerType": 128
        }
    ],
    "properties": {},
    "buildNumberFormat": "$(date:yyyyMMdd)$(rev:.r)",
    "process": {
        "phases": [
            {
                "steps": [],
                "name": "All-Apps-Integration-CI",
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
    "name": "integration-CI",
    "path": "\\",
    "type": 2
}