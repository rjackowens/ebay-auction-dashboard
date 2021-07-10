FROM ubuntu:latest

RUN apt-get update
RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app

RUN apt-get install python3-setuptools -y
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN python3 -m pip --trusted-host pypi.org --trusted-host files.pythonhosted.org install -r requirements.txt

COPY . .

ENV celery_broker_url=redis://redis:6379

EXPOSE 8080 6379

ENTRYPOINT [ "python3", "./server.py" ]
