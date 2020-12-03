FROM ubuntu as builder
MAINTAINER lpshkn

RUN apt-get update && apt-get install -y python3 \
    && apt-get install -y python3-setuptools \
    && apt-get install -y python3-pip \
    && apt-get install -y locales \
    && apt-get install -y language-pack-ru

COPY requirements.txt .
ENV DEBIAN_FRONTEND noninteractive
ENV LANGUAGE ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
RUN pip3 install -r requirements.txt && locale-gen ru_RU.UTF-8 \
    && dpkg-reconfigure locales


FROM builder
MAINTAINER lpshkn

COPY . /Ataurus
WORKDIR /Ataurus

RUN nosetests --with-coverage --cover-package=ataurus && python3 setup.py install
ENTRYPOINT ["Ataurus"]
