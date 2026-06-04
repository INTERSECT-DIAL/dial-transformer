{{/*
Return the proper dial-transformer image name
*/}}
{{- define "dial-transformer.image" -}}
{{- include "common.images.image" (dict "imageRoot" .Values.dialTransformer.image "global" .Values.global) -}}
{{- end -}}

{{/*
Return the proper Container Image Registry secret names
*/}}
{{- define "dial-transformer.imagePullSecrets" -}}
{{- include "common.images.renderPullSecrets" (dict "images" (list .Values.dialTransformer.image) "context" $) -}}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "dial-transformer.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "common.names.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}
