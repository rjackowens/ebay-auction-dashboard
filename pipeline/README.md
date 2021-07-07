## Pipeline Readme
Resources used by Tekton to run teams-status build pipeline

![](.\pipeline-diagram.png)


#### **Overview**
 Creates `Pipeline`, `PipelineRun`, `TriggerBindings`, `Secret`, and `PersistentVolumeClaim` resources in OpenShift


#### **Usage**
- Pipeline triggers automatically on commit/creation of feature branch
- Manually trigger pipeline run via `tkn pipeline start teams-status-pipeline`


#### **Features**
- Performs YAML validation of deployment resources using `yamllint` 
- Builds and pushes tagged Docker image using `buildah`
- Triggers Argo CD deployment after successful build
