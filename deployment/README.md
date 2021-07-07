## Deployment Readme
Resources used by Argo CD to deploy teams-status app into OpenShift

![](.\deployment-diagram.png)


#### **Overview**
 Creates `deployment`, `service`, `route`, `config` and `secret` resources in OpenShift
- Pulls latest image from Quay registry here: https://quay.apps.np2.ent-ocp4-np2-useast1.aws.internal.das/repository/payeros/teams-status
- Deploys 1 pod with `revisionHistoryLimit` set to 3
<br>


#### **Accessing External Endpoint**
This app is externally accessible at "http://teams-status-route-payeros-devops.apps.np1.ent-ocp4-np1-useast1.aws.internal.das"
<br>


#### **Viewing App Logs**
 1. Go to https://console-openshift-console.apps.np1.ent-ocp4-np1-useast1.aws.internal.das/k8s/ns/payeros-devops/deployments/teams-status-app/pods.
 2. Select the pod name and click on the *Logs* tab
<br>


#### **Storing Config Values**
 Config values are passed to OpenShift containers as environment variables. To add new config values:
 1. Add new key/value pair to `config.yml`
	```YAML
	data:
		my-config: "Hello World!"
	```
 2. Add config value to `deployment.yml` under `env`

	```YAML
	   - name: MY_CONFIG
	    	valueFrom:
		    	configMapKeyRef:
			    	name: teams-status-config
			    	key: my-config
	```
3. Reference config value as environment variable in application. Example:
	```Python
	   myconfig = os.environ["MY_CONFIG"]
	```
<br>


#### **Managing Secrets**
 Secrets are passed to OpenShift containers as environment variables. To add a new secret:
 1. Navigate to `kv/data/teams-status` in [Vault](https://vault.acr.awsdns.internal.das/)
 2. Add new key/value pair to Vault secret JSON
	```JSON
	{
		"my-secret": "Hello World"
	}
	```
 2. Add the key/value pair to `secrets.yml`. The OpenShift key name should match the Vault key name. The Vault key name should be followed by `| base64encode` and enclosed in `<>`.
	```YAML
	data:
		my-secret: <my-secret | base64encode>
	```
	
 3. Add secret to `deployment.yml` under `env`
	```YAML
	   - name: MY_SECRET
	    	valueFrom:
		    	secretKeyRef:
			    	name: teams-status-secrets
			    	key: my-secret
	```
4. Reference secret as environment variable in application. Example:
	```Python
	   mysecret = os.environ["MY_SECRET"]
	```
<br>


#### **Mounting Certificates**
 Certificates are mounted to OpenShift containers as volumes. To add a new certificate:
 1. Download certificate as base64-encoded `.cer` file. Instructions are available [here](https://www.esri.com/arcgis-blog/products/bus-analyst/field-mobility/learn-how-to-download-a-ssl-certificate-for-a-secured-portal/)
 2. Navigate to `kv/data/teams-status` in [Vault](https://vault.acr.awsdns.internal.das/)
 3. Add new key/value pair to Vault secret JSON
	```JSON
	{
		"my-cert": "<base64 encoded string>"
	}
	```
 4. Add the key/value pair to `secrets.yml`. The OpenShift key name should match the Vault key name. The Vault key name should be followed by `| base64encode` and enclosed in `<>`.
	```YAML
	data:
		my-cert: <my-cert | base64encode>
	```
 5. Add cert to `deployment.yml` under `volumeMounts`. The `mountPath` specifies where the cert is mounted to the container, `subPath` refers to the key name of the cert in `secrets.yml`.

	```YAML
        - mountPath: /app/<directory_to_mount>
          subPath: my-cert
          name: example-cert
          readOnly: true
	```
 4. Add cert to `deployment.yml` under `volumes`. 

	```YAML
		- name: example-cert
			secret:
				secretName: teams-status-secrets
	```
Your cert is now mounted at the `mountPath` specified above in the container.
<br>


#### **Manual Deployment**
- This app is automatically deployed via Argo CD webhook
- For manual deployment to a specific environment, run `.\scripts\manual-deployment.ps1`
<br>
