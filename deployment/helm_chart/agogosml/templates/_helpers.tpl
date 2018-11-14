{{/* vim: set filetype=mustache */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "data-pipeline-app.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "data-pipeline-app.fullname" -}}
{{- $name := .Chart.Name -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "data-pipeline-app.input_reader.fullname" -}}
{{ include "data-pipeline-app.fullname" . | printf "%s-in-rdr" }}
{{- end -}}

{{- define "data-pipeline-app.instance-app.fullname" -}}
{{ include "data-pipeline-app.fullname" . | printf "%s-ia" }}
{{- end -}}

{{- define "rbac.version" }}rbac.authorization.k8s.io/v1beta1{{ end -}}