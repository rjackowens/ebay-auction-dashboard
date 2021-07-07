## README
This app polls Tekton pipelines and reports the build status to the [Build-Status](https://teams.microsoft.com/l/channel/19%3ad9f5ba9051524250b6b5b2ea0d34dd57%40thread.tacv2/Build-Status?groupId=0ff486f5-40c8-4b44-a499-9ea13f15c7be&tenantId=be8c08f2-ac07-442c-9a46-ebeeeb5bd4d7) Teams channel


![](.\diagrams\sequence-diagram.png)


#### **App Components**
![](.\diagrams\components.png)


#### **Starting Docker Container**
docker build . -t status-dashboard; docker run -it -p 8080:8080 status-dashboard
