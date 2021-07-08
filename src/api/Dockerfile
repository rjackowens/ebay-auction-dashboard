FROM selenium/standalone-chrome
USER root

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install python3-setuptools -y

COPY requirements.txt .
RUN python3 -m pip --trusted-host pypi.org --trusted-host files.pythonhosted.org install -r requirements.txt

COPY . .

ENV celery_broker_url=redis://redis:6379
EXPOSE 9000 6379

USER seluser

# start flask server
ENTRYPOINT [ "python3", "./server.py" ]
