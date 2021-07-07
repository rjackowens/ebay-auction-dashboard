FROM ubuntu:latest

#### oc CLI ####
RUN apt-get update
RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_11.x  | bash -
RUN apt-get -y install nodejs

RUN apt-get install -y wget && \
    apt-get install -y tar

RUN wget --no-check-certificate https://github.com/openshift/origin/releases/download/v3.7.0/openshift-origin-client-tools-v3.7.0-7ed6862-linux-64bit.tar.gz
RUN tar -xzf openshift-origin-client-tools-v3.7.0-7ed6862-linux-64bit.tar.gz
RUN ln -s /openshift-origin-client-tools-v3.7.0-7ed6862-linux-64bit/oc /bin/oc

#### tkn CLI ####
COPY tkn-linux-amd64-0.11.0.tar.gz .
RUN tar xvzf tkn-linux-amd64-0.11.0.tar.gz
RUN cp tkn bin

#### python ####
RUN apt-get update && apt-get install -y python3 python3-pip

#### runtime ####
RUN mkdir ./.kube && touch ./.kube/config
RUN chmod 777 ./.kube/config

RUN mkdir /data && chmod 777 /data
RUN adduser --disabled-password --gecos "" redis
RUN chown redis /data

WORKDIR /app

RUN apt-get install python3-setuptools -y
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN python3 -m pip --trusted-host pypi.org --trusted-host files.pythonhosted.org install -r requirements.txt

COPY . .

# local testing only
ENV automation_token=eyJhbGciOiJSUzI1NiIsImtpZCI6Ijltc1ltWjVIaEpINXFTQ1FjdlAtOFFuTUllV05DNmNOWXNHSDRDQmhqM0kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJwYXllcm9zLWRldm9wcyIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJjaWNkLWF1dG9tYXRpb24tc2VydmljZS10b2tlbi1mZGg5dCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50Lm5hbWUiOiJjaWNkLWF1dG9tYXRpb24tc2VydmljZSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjUzZWIyMDZjLWNhMmItNDQ2NS04NjRlLWMyMzA3N2Q1MTc2NSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpwYXllcm9zLWRldm9wczpjaWNkLWF1dG9tYXRpb24tc2VydmljZSJ9.nBOgwd_A2w458-08NuKDRCmOhHl6HgMp7VzHGiwyxAQirUTMOlIJrGyBi4Y2Tzv5DcIlMpIu5ochigs0XKskXiVV8zE9tHmML4ba0kv3vYyrxcZpKhZDQeBN4cIUqvbYwX5dctEHBLXVHJA5-4qCniXQP0VYDQeOvorB1Dh_oUCPq8xJnrjCrG8kLvDZDcMVM9filgXWUoU0mI_28vMG2VDh2MQ4abvTErI-I87EZgTcGhVbb-6B0tLHCRvRxsgZovBU422HebBdX_5PtJNWDvI19pCMbxGebNNRU3TvEZvVZ5wvDvQ8N-1ifqp5WtpObAyn1WcaXgZapzkin1KNEQ
ENV teams_webhook_url=https://wellpoint.webhook.office.com/webhookb2/0ff486f5-40c8-4b44-a499-9ea13f15c7be@be8c08f2-ac07-442c-9a46-ebeeeb5bd4d7/IncomingWebhook/64f8720320294d6a8e7cd3e821f8eb2a/b10a7a2b-64ed-42b3-970d-7009b07f7c69
ENV openshift_cluster_url=https://api.np1.ent-ocp4-np1-useast1.aws.internal.das:6443
ENV openshift_logs_url=https://console-openshift-console.apps.np1.ent-ocp4-np1-useast1.aws.internal.das/k8s/ns/payeros-devops/tekton.dev~v1beta1~PipelineRun/
ENV celery_broker_url=redis://redis:6379

EXPOSE 8080 6379

ENTRYPOINT [ "python3", "./server.py" ]
