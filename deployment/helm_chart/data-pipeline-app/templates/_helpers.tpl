{{/* vim: set filetype=mustache */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "data-pipeline-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "data-pipeline-app.fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "data-pipeline-app.input_reader.fullname" -}}
{{ include "data-pipeline-app.fullname" . | printf "%s-in-rdr" }}
{{- end -}}

{{- define "data-pipeline-app.business-logic.fullname" -}}
{{ include "data-pipeline-app.fullname" . | printf "%s-bl" }}
{{- end -}}

{{- define "data-pipeline-app.cli.fullname" -}}
{{ include "data-pipeline-app.fullname" . | printf "%s-cli" }}
{{- end -}}

{{- define "rbac.version" }}rbac.authorization.k8s.io/v1beta1{{ end -}}