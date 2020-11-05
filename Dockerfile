FROM ubuntu
MAINTAINER lpshkn

RUN apt-get update && apt-get install -y python3 \
    && apt-get install -y python3-setuptools \
    && apt-get install -y python3-pip

COPY . /Ataurus
WORKDIR /Ataurus

RUN pip3 install -r requirements.txt && python3 setup.py test
ENTRYPOINT ["python3", "./ataurus/main.py"]