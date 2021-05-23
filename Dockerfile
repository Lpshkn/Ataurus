FROM python:3.9.2-slim-buster
MAINTAINER lpshkn

COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

COPY . /ataurus
WORKDIR /ataurus

RUN mkdir -p result/features result/model

ENTRYPOINT ["python3", "./ataurus/main.py"]