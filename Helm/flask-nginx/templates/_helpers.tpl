{{- define "flask-nginx.name" -}}
{{- .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{- define "flask-nginx.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}

{{- define "flask-nginx.labels" -}}
app.kubernetes.io/name: {{ include "flask-nginx.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

